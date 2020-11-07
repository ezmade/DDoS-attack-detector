document.getElementById('setModelname').onclick = getModelname

async function getModelname()
{
    let modelname = document.getElementById('model').value;
    console.log(modelname);
    return(modelname)
}