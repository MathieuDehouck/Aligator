

function save(feedback) {
    console.log(JSON.stringify(feedback));

    var fb = document.getElementById('feedback_'+feedback);
    var jk = document.getElementById('joke_'+feedback);
    var x = document.querySelector('input[name="rate'+feedback+'"]:checked');
    if (x) var x = x.value;
    console.log(x)

    var comp = document.querySelector('input[name="comp'+feedback+'"]').value;
    var sens = document.querySelector('input[name="sensible'+feedback+'"]').value;
    var rem = document.querySelector('input[name="remarks'+feedback+'"]').value;
    
    console.log(comp, sens, rem)

    console.log(jk)

    //fs.writeFile('test', x)

}
