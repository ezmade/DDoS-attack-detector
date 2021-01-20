document.getElementById('startClassification').onclick = startClassification

async function startClassification()
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

    let response = await fetch('classificate-data',{
        method: 'POST',
        body: formData
        }
    );
    console.log(response);
}