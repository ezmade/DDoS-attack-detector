document.getElementById('send').onclick = sendFile

async function sendFile()
{
    let filename = document.getElementById('file');
    if (!filename.value)
    {
        alert('Укажите имя файла!');
        return
    }
    const formData = new FormData();
    let file = filename.files[0];
    console.log(file);
    formData.append('file', file);

    let response = await fetch('classificate-data',{
        method: 'POST',
        body: formData
        }
    );
    console.log(response);

    let outFilename = await response.text();

    console.log(outFilename);
}