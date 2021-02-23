from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
# from .forms import UploadFileForm
from .forms import FrameFormSet, UploadForm, GenerateCForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def home(request):
    template_name = 'base.html'
    return render(request, template_name)

def news(request):
    template_name = 'base.html'
    return render(request, template_name)

def tools(request):
    # import cantools
    # generate_c_source()
    # from pprint import pprint
    # db = cantools.database.load_file('C:/Users/acront/Desktop/autosar_tools/autosar_tools/myapp/FBL_MLBevo_Gen2_MLBevo_HCAN_KMatrix_V8.18.01F_20190718_SE.dbc')
    # example_message = db.get_message_by_name('BMS_MV_02')
    # print(db.get_message_by_name('BMS_MV_01'))
    # pprint(example_message.signals)
    template_name = 'autosar_tools/tools.html'
    return render(request, template_name)

def tool_request(request):
    template_name = 'base.html'
    return render(request, template_name)

def frame_extract(request):
    template_name = 'autosar_tools/create.html'
    data = dict()
    if request.method == 'POST':
        formset = FrameFormSet(request.POST)
        fileform = UploadForm(request.POST, request.FILES)

        if formset.is_valid() and fileform.is_valid():
            frames = []
            for form in formset:
                name = form.cleaned_data.get('name')
                cyclicity = form.cleaned_data.get('cyclicity')
                # save book instance
                if name:
                    line = []
                    line.append(name)
                    line.append(cyclicity)
                frames.append(line)
            # for each frame append an empty array to add the timing from the uploaded file
            for frame in frames:
                frame.append([])

            #get the data from the uploaded file
            content = ""
            upFile = request.FILES['file']
            if not upFile.multiple_chunks():
                content = upFile.read()
            else:
                for chunk in upFile.chunks():
                    content += chunk

            #convert the content from binary to string
            content = content.decode('ascii').split("\r\n")

            #extract the timings from file of each signal and add it to the frames array
            data['frames_not_found'] = []
            data['frames_found'] = []
            for frame in frames:
                for line in content:
                    line_content = line.split()
                    if frame[0] in line_content:
                        frame[2].append(line_content[0])
                if not frame[2]:
                    data['frames_not_found'].append(frames.index(frame))
                else:
                    data['frames_found'].append(frames.index(frame))
                    # data['frames_not_found'] += str(frames.index(frame)) + " "

            if len(data['frames_not_found']) == 0:
                data['form_is_valid'] = True
                #pass the array with the frames to the session to create the output file in the download page
                request.session['frames'] = frames
                # #pass the filename to the session to name the output file in the download page
                request.session['fileName'] = upFile.name.split(".")[0]
                return JsonResponse(data)
            else:
                data['form_is_valid'] = False
                return JsonResponse(data)
    else:
        formset = FrameFormSet()
        fileform = UploadForm()
    return render(request, template_name, {
        'formset': formset,
        'fileform': fileform,
    })

def frame_extract_download(request):
    # template_name = 'autosar_tools/download.html'

    # if request.method == 'POST':
    frames = request.session.get('frames')
    request.session['frames'] = []
    fileName = request.session.get('fileName')
    request.session['fileName'] = []
    print(request.session['frames'])
    print(request.session['fileName'])
        # if 'excel' in request.POST:
    import xlwt
    
    # Creating a workbook 
    aux_book = xlwt.Workbook()
    style_percent = xlwt.easyxf(num_format_str='0.00%')

    # Adding a sheet of name "Sheet1" to the workbook
    ws = aux_book.add_sheet('Sheet1', cell_overwrite_ok=True)
    # variable i is used to go through the columns of the workbook
    i = 0
    for frame in frames:
        ws.write_merge(0, 0, i, i + 2, frame[0])
        ws.write(1, i, 'Time')
        ws.write(1, i + 1, 'Delta')
        ws.write(1, i + 2, 'Error')
        # variable j is used to go through the lines of the workbook
        j = 2
        prev_time = float(0)
        for time in frame[2]:
            ws.write(j, i, float(time))
            ws.write(j, i + 1, float(time) - prev_time)
            ws.write(j, i + 2, (float(frame[1]) - (float(time) - prev_time)) / float(frame[1]), style_percent)
            prev_time = float(time)
            j = j + 1
        # remove the content of Delta and Error cell for the first time of each frame
        ws.write(2, i + 1, '')
        ws.write(2, i + 2, '')
        i = i + 4

    # Create the HttpResponse object with the appropriate headers.
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + fileName + "_result.xls"

    # save to buffer
    aux_book.save(response)
    return response

    # return render(request, template_name)

def generate_c_source(request):
    template_name = 'autosar_tools/generateC.html'
    data = dict()
    if request.method == 'POST':
        form = GenerateCForm(request.POST)
        fileform = UploadForm(request.POST, request.FILES)

        if form.is_valid() and fileform.is_valid():
            import cantools
            from cantools.database.can.c_source import generate
            dbase = cantools.database.load_file('C:/Users/acront/Desktop/autosar_tools/autosar_tools/myapp/FBL_MLBevo_Gen2_MLBevo_HCAN_KMatrix_V8.18.01F_20190718_SE.dbc')

            database_name = 'FBL_MLBevo_Gen2_MLBevo_HCAN_KMatrix_V8.18.01F_20190718_SE'

            filename_h = database_name + '.h'
            filename_c = database_name + '.c'
            fuzzer_filename_c = database_name + '_fuzzer.c'
            fuzzer_filename_mk = database_name + '_fuzzer.mk'

            header, source, fuzzer_source, fuzzer_makefile = generate(
                dbase,
                database_name,
                filename_h,
                filename_c,
                fuzzer_filename_c,
                form.cleaned_data['floating_point_numbers'],
                form.cleaned_data['bit_fields']
                )

            with open(filename_h, 'w') as fout:
                fout.write(header)

            with open(filename_c, 'w') as fout:
                fout.write(source)

            print('Successfully generated {} and {}.'.format(filename_h, filename_c))

            if form.cleaned_data['generate_fuzzer']:
                with open(fuzzer_filename_c, 'w') as fout:
                    fout.write(fuzzer_source)

                with open(fuzzer_filename_mk, 'w') as fout:
                    fout.write(fuzzer_makefile)

                # print('Successfully generated {} and {}.'.format(fuzzer_filename_c,
                #                                                  fuzzer_filename_mk))
                # print()
                # print(
                #     'Run "make -f {}" to build and run the fuzzer. Requires a'.format(
                #         fuzzer_filename_mk))
                # print('recent version of clang.')
            print(form.cleaned_data['floating_point_numbers'])
            print("dwsdwff")
            print(form.cleaned_data['bit_fields'])
            print()
            print(form.cleaned_data['generate_fuzzer'])
    else:
        form = GenerateCForm(use_required_attribute=False)
        fileform = UploadForm()
    return render(request, template_name, {
        'form': form,
        'fileform': fileform,
    })