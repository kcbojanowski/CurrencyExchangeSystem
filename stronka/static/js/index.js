const Selectors = document.querySelectorAll("form select"),
fromCurrency = document.querySelector(".from select"),
amountCurrency = document.querySelector(".amount input"),
toCurrency = document.querySelector(".to select"),
getButton = document.querySelector("form .btn-index");

for (let i = 0; i < Selectors.length; i++) {
    for(let currency_code in country_list){
        let selected = i === 0 ? currency_code === "USD" ? "selected" : "" : currency_code === "PLN" ? "selected" : "";
        let optionTag = `<option value="${currency_code}" ${selected}>${currency_code}</option>`;
        Selectors[i].insertAdjacentHTML("beforeend", optionTag);
    }
    Selectors[i].addEventListener("change", e =>{
        loadFlag(e.target);
    });
}

function loadFlag(element){
    for(let code in country_list){
        if(code === element.value){
            let flagTag = element.parentElement.querySelector("span");
            flagTag.className = `fi fi-${country_list[code]}`;
        }
    }
}
window.addEventListener("load", ()=>{
    getExchangeRate();
});

getButton.addEventListener("click", e =>{
    e.preventDefault();
    getExchangeRate();
});

const exchangeIcon = document.querySelector("form .exchange");
exchangeIcon.addEventListener("click", e=>{
    e.preventDefault();
    let temp = fromCurrency.value;
    fromCurrency.value = toCurrency.value;
    toCurrency.value = temp;
    loadFlag(fromCurrency);
    loadFlag(toCurrency);
    getExchangeRate();
})


function getExchangeRate(){
    const amount = document.querySelector("form input");
    const fromCurrencyTxt = document.querySelector(".from-rate");
    const exchangeRateTxt = document.querySelector(".exchange-rate");
    const showcaseTitle = document.querySelector(" .exchange-title");
    let amountVal = amountCurrency.value;

    if(amountVal === "" || amountVal === "0"){
        amount.value = "1";
        amountVal = 1;
    }
    exchangeRateTxt.innerText = "0.00";
    let url = `https://api.frankfurter.app/latest?amount=${amountVal}&from=${fromCurrency.value}&to=${toCurrency.value}`;
    fetch(url)
        .then(response => response.json())
        .then(result =>{

        let totalExRate = result.rates[toCurrency.value];
        fromCurrencyTxt.innerText = `${amountVal} ${fromCurrency.value} =`;
        exchangeRateTxt.innerText = `${totalExRate} ${toCurrency.value}`;
        showcaseTitle.innerHTML = `${fromCurrency.value} 
                                    <span class="fi fi-${country_list[fromCurrency.value]}"></span>
                                     <i class="fa-solid fa-arrow-right-arrow-left"></i> 
                                    ${toCurrency.value} 
                                    <span class="fi fi-${country_list[toCurrency.value]}"></span>`
    }).catch(() =>{
        exchangeRateTxt.innerHTML = "<i class=\"fa-solid fa-circle-exclamation\"></i>";
    });
}