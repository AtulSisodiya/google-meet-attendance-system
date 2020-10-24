const timeArr = Array();
let formJsonData = {};
let finalData = [];
let count = 0;
let renderCount = 0;
let renderList = []

class renderEle {
    constructor(no) {
        this.root = document.getElementById("drag-root");
        this.curLi = document.createElement("li")
        this.liHook = document.getElementById(`${no}`)
        this.curLi.classList.add("drag-column");
        this.curLi.id = `cl${no}`
    }
    intialRender(headerData, no) {
        let data = `
                <div class="button-container">
                    <button type="submit" onclick="sendDataList(this)" class="list-btn-submit">&#10004;</button>
                </div>
                <span class="drag-column-header">
                    ${headerData}
                </span>
                <ul class="drag-inner-list" id="${no}">
                    <div  class="loader center"></div>
                </ul>
        
        `
        this.root.appendChild(this.curLi)
        this.curLi.innerHTML = data;
        this.liHook = document.getElementById(`${no}`)
        this.colHeader = this.curLi.getElementsByClassName("drag-column-header")[0]
    }
    createLi(lidata) {
        let liEle = document.createElement("li")
        liEle.classList.add("drag-item");
        liEle.innerHTML = lidata;
        this.liHook.appendChild(liEle);
    }
    addLi(listNames) {
        for (const i of listNames) {
            this.createLi(i)
        }
    }
}

const convertFrom24To12Format = (time24) => {
    const [sHours, minutes] = time24.match(/([0-9]{1,2}):([0-9]{2})/).slice(1);
    const period = +sHours < 12 ? 'AM' : 'PM';
    const hours = +sHours % 12 || 12;

    return `${hours}:${minutes} ${period}`;
}



async function getJsonData(par) {
    if (par) {
        const data = await eel.returnJsonData(par)();
        return data
    }
    const data = await eel.returnJsonData()();
    return data;
}

window.onload = async function () {
    data = await getJsonData("isremember");
    console.log(data);
    if (strFillter(data) === "on") {
        var date = new Date();
        var currentTime = date.getHours() + ':' + date.getMinutes();
        document.getElementById("appt").value = currentTime;
        document.getElementsByTagName("form")[0].parentElement.classList.add("hide");
        document.getElementsByTagName("form")[1].parentElement.classList.remove("hide");
    }
    console.log("after");
}

window.oncontextmenu = function () {
    return false;
}
document.onkeydown = function (e) {
    if (window.event.keyCode == 123 || e.button == 2)
        return false;
}

document.getElementsByTagName("form")[0].addEventListener("submit", (e) => {
    e.preventDefault();
    let formData = new FormData(e.target)
    if (!formData.has("isremember")) {
        formData.set("isremember", "off")
    }
    formJsonData = JSON.stringify(Object.fromEntries(formData));
    document.getElementsByTagName("form")[0].parentElement.classList.add("hide");
    document.getElementsByTagName("form")[1].parentElement.classList.remove("hide");
})
document.getElementsByTagName("form")[1].addEventListener("submit", (e) => {
    e.preventDefault();
    if (Object.keys(formJsonData).length) {
        formJsonData = JSON.stringify({ ...(Object({ "meeting_url": e.target[0].value, "times": timeArr })), ...JSON.parse(formJsonData) });
    }
    else {
        formJsonData = JSON.stringify({
            ...(Object({ "meeting_url": e.target[0].value, "times": timeArr }))
        })
    }
    document.getElementsByTagName("form")[1].parentElement.classList.add("hide");
    document.getElementById("drag-root").classList.remove("hide");
    timeArr.forEach((element, index) => {
        let newList = new renderEle(index);
        newList.intialRender(convertFrom24To12Format(element), index);
        renderList.push(newList);
        count++;
    });
    handleDrag();
    startTask();
})




async function getDir() {
    const data = await eel.get_directory()();
    document.getElementById("output").value = data
}


function strFillter(st) {
    return st.replace(/"/g, "")
}

eel.expose(sendFormData);

function sendFormData() {
    return formJsonData;
}
eel.expose(render);
function render(par) {
    console.log(par)
    let listHook = renderList[renderCount];
    listHook.curLi.querySelector(".loader").classList.add("hide")
    listHook.colHeader.innerHTML = par[0][0]
    listHook.addLi(par[0].slice(1,))
    renderCount++;
    console.log(par);
}

async function startTask() {
    await eel.changeJsonData()();
    let data = await eel.returnJsonData()();
    console.log(data);
    await eel.start_timers()();

}
eel.expose(get_final_data)
function get_final_data() {
    return finalData;
}

async function sendDataList(par) {
    const el = par.closest("li");
    finalData.push(el.getElementsByClassName("drag-column-header")[0].textContent)
    let liArr = Array(...el.getElementsByClassName("drag-item"))
    liArr.forEach(ele => {
        finalData.push(ele.textContent);
    })
    finalData = finalData.sort()
    await eel.save_excel(finalData)();
    document.getElementsByClassName("drag-container")[0].classList.add("hide")
    document.getElementsByClassName("final-msg")[0].classList.remove("hide")
    console.log(finalData.sort());
}
function close() {
    window.close()
}