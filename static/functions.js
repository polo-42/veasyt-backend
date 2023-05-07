function convert_SP_to_chf(value){
    var value_input = document.getElementById('Sp_to_convert').value;
    var result = addZeroes(value_input * value);
    document.getElementById('converted_value').innerHTML = result;
    document.getElementById('CHF_plus').innerHTML = "+"+result;
    document.getElementById('SP_minus').innerHTML = "-"+value_input;
}

function substract_balance_chf(){
    var value_input = document.getElementById('CHF_to_validate').value;
    var result = addZeroes(value_input);
    document.getElementById('CHF_minus').innerHTML = "-"+result;
}

function addZeroes(num) {
    return num.toLocaleString("en", {useGrouping: false, minimumFractionDigits: 2})
}
 