function handleDrag(){
	dragula([
	document.getElementById('0'),
	document.getElementById('1'),
	document.getElementById('2'),
	document.getElementById('3'),
	document.getElementById('4'),
	document.getElementById('5')
])

.on('drag', function(el) {
	
	// add 'is-moving' class to element being dragged
	el.classList.add('is-moving');
})
.on('dragend', function(el) {
	
	// remove 'is-moving' class from element after dragging has stopped
	el.classList.remove('is-moving');
	
	// add the 'is-moved' class for 600ms then remove it
	window.setTimeout(function() {
		el.classList.add('is-moved');
		window.setTimeout(function() {
			el.classList.remove('is-moved');
		}, 600);
	}, 100);
});
}






function alertClose(par) {
	console.log(par);

	const timeData = (par.closest(".alert").children[0].children[0].textContent)
	console.log(timeData);
	const index = timeArr.indexOf(timeData);
	if (index > -1) {
		timeArr.splice(index,1);
	}
	par.closest(".alert").remove();
}

function addBtn() {
	const time =(document.getElementById("appt").value);
	if (timeArr.includes(time)) {
		return
	}
	console.log("hello");
	timeArr.push(time);
	const newEle = document.createElement("div");
	newEle.classList.add("alert");
	newEle.innerHTML = `
    <div>
            <p>${convertFrom24To12Format(time)}</p>
    </div>
        <div class="alert-close-btn" onclick="alertClose(this)">X</div>
    `
	document.getElementById("time-hook").appendChild(newEle);

}
