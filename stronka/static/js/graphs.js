const SelectGraph = document.querySelectorAll("form select"),
graphButton = document.querySelector("form .btn-index");

for (let i = 0; i < SelectGraph.length; i++) {
    for(let currency_code in country_list){
        let selected = i === 0 ? currency_code === "USD" ? "selected" : "" : currency_code === "PLN" ? "selected" : "";
        let optionTag = `<option value="${currency_code}" ${selected}>${currency_code}</option>`;
        SelectGraph[i].insertAdjacentHTML("beforeend", optionTag);
    }
    SelectGraph[i].addEventListener("change", e =>{
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