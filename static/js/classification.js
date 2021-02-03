document.getElementById('start_classification').onclick = start_classification

async function start_classification()
{
    let filename = document.getElementById('input_file');
    let modellist = document.getElementById('classification_model');

    if (!filename.value)
    {
        alert('Укажите имя файла!');
        return
    }
    const formData = new FormData();
    let file = filename.files[0];
    let modelname = modellist.value;
    console.log(file, modelname);
    formData.append('file', file);
    formData.append('modelname', modelname);

    let response = await fetch('classification',{
        method: 'POST',
        body: formData
        }
    );
    console.log(response);
}