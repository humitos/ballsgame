var ws = $.websocket(websocket_url);

function isContained(m, e){
    var e=e||window.event
    var c=/(click)|(mousedown)|(mouseup)/i.test(e.type)? e.target : ( e.relatedTarget || ((e.type=="mouseover")? e.fromElement : e.toElement) )
    while (c && c!=m)try {c=c.parentNode} catch(e){c=m}
    if (c==m)
	return true
    else
	return false
}

window.addEventListener('load', function(){
    
    var box1 = document.getElementById('box1')
    var statusdiv = document.getElementById('statusdiv')

    var startx = 0
    var starty = 0
    var distx = 0
    var disty = 0

    var detecttouch = !!('ontouchstart' in window) || !!('ontouchstart' in document.documentElement) || !!window.ontouchstart || !!window.Touch || !!window.onmsgesturechange || (window.DocumentTouch && window.document instanceof window.DocumentTouch)
    var ismousedown = false
    
    box1.addEventListener('touchstart', function(e){
	var touchobj = e.changedTouches[0] // reference first touch point (ie: first finger)
	startx = parseInt(touchobj.clientX)
	starty = parseInt(touchobj.clientY)
	statusdiv.innerHTML = 'Status: touchstart<br /> ClientX: ' + startx + 'px';
	ws.send(nickname,  {"type": "startx", "value": startx});
	ws.send(nickname,  {"type": "starty", "value": starty});
	e.preventDefault()
    }, false)
    
    box1.addEventListener('touchmove', function(e){
	var touchobj = e.changedTouches[0] // reference first touch point (ie: first finger)
	var distx = parseInt(touchobj.clientX) - startx
	statusdiv.innerHTML = 'Status: touchmove<br /> Horizontal distance traveled: ' + distx + 'px'
	ws.send(nickname, {"type": "distx", "value": distx});

	var disty = parseInt(touchobj.clientY) - starty
	statusdiv.innerHTML = 'Status: touchmove<br /> Vertical distance traveled: ' + disty + 'px'
	ws.send(nickname, {"type": "disty", "value": disty});

	e.preventDefault()
    }, false)
    
    box1.addEventListener('touchend', function(e){
	var touchobj = e.changedTouches[0] // reference first touch point (ie: first finger)
	statusdiv.innerHTML = 'Status: touchend<br /> Resting x coordinate: ' + touchobj.clientX + 'px'
	e.preventDefault()
    }, false)
    
    if (!detecttouch){
	
	document.body.addEventListener('mousedown', function(e){
	    if ( isContained(box1, e) ){
		var touchobj = e
		ismousedown = true
		startx = parseInt(touchobj.clientX)
		starty = parseInt(touchobj.clientY)
		statusdiv.innerHTML = 'Status: touchstart<br /> ClientX: ' + startx + 'px';
		ws.send(nickname, {"type": "startx", "value": startx});
		ws.send(nickname, {"type": "starty", "value": starty});
		e.preventDefault()
	    }
	}, false)
	
	document.body.addEventListener('mousemove', function(e){
	    if (ismousedown){
		var touchobj = e
		var distx = parseInt(touchobj.clientX) - startx
		statusdiv.innerHTML = 'Status: touchmove<br /> Horizontal distance traveled: ' + distx + 'px'
		ws.send(nickname, {"type": "distx", "value": distx});

		var disty = parseInt(touchobj.clientY) - starty
		statusdiv.innerHTML = 'Status: touchmove<br /> Vertical distance traveled: ' + disty + 'px'
		ws.send(nickname, {"type": "disty", "value": disty});
		e.preventDefault()
	    }
	}, false)
	
	document.body.addEventListener('mouseup', function(e){
	    var touchobj = e
	    ismousedown = false
	    statusdiv.innerHTML = 'Status: touchend<br /> Resting x coordinate: ' + touchobj.clientX + 'px'
	    e.preventDefault()
	}, false)
	
	
    }
    
}, false)
