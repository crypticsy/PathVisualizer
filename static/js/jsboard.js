window.jsboard = (function(){

    'use strict';

    // constr
    function Board(props,size,attached) {

        var matrixForm = [];

        var methods = {

            // return matrix form of game board
            matrix: function() {
                while (matrixForm.length>0) { matrixForm.pop(); }
                for (var r=0; r<props.childNodes.length; r++) {
                    matrixForm.push([]);
                    for (var c=0; c<props.childNodes[0].childNodes.length; c++) {
                        if (typeof props.childNodes[r].childNodes[c].childNodes[0] != "undefined") {
                            matrixForm[r].push(props.childNodes[r].childNodes[c].childNodes[0].innerHTML);
                        }
                        else { matrixForm[r].push(null); }
                    }
                }
                return matrixForm;
            },
            // return rows
            rows: function() { return size[0]; },
            // return cols
            cols: function() { return size[1]; },
            // change board style
            style: function(props) {
                for (var st in props) {
                    document.getElementById(attached).style[st] = props[st];
                }
            },
            // remove all event listeners on board
            removeEvents: function(ev, func) {
                for (var i=0; i<document.getElementsByTagName("td").length; i++) {
                    document.getElementById(attached).getElementsByTagName("td")[i].removeEventListener(ev, func);
                }
            },
            // inner cell functions
            cell: function(arr, move) {
                // get DOM node for given row and col
                function getBoardCell(row,col) {
                    return document.getElementById(attached).getElementsByClassName("boardRow_"+row)[0].childNodes[col];
                }
                // get DOM node from given data attribute
                function getObjFromDataAtr(pl) {
                    var wh = pl.split("x");
                    wh[0] = parseInt(wh[0]);
                    wh[1] = parseInt(wh[1]);
                    if (move) {
                        var r = movePieceInMatrix(move,[wh[0],wh[1]]);
                        wh[0] = r[0]; wh[1] = r[1];
                    }
                    return [wh[0],wh[1]];
                }
                // move cell around matrix like so: b.cell(this,-12)
                function movePieceInMatrix(keepDec,wh) {
                    if (keepDec<0) {
                        while (keepDec<0) {
                            if (wh[1]>0) { wh[1] -= 1; }
                            else { wh[1] = size[1]-1; wh[0] -= 1; }
                            keepDec++;
                        }
                    }
                    else {
                        while (keepDec>0) {
                            if (wh[1]<size[1]-1) { wh[1] += 1; }
                            else { wh[1] = 0; wh[0] += 1; }
                            keepDec--;
                        }
                    }
                    return [wh[0],wh[1]];
                }
                var cellMethods = {
                    DOM: function() {
                        if (typeof arr[0] == "number") {
                            if (arr[0]<0||arr[1]<0||arr[0]>size[0]-1||arr[1]>size[1]-1) { return document.createElement("div"); }
                            return document.getElementById(attached).getElementsByClassName("boardRow_"+arr[0])[0].childNodes[arr[1]];
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return document.createElement("div"); }
                            var th = getBoardCell(wh[0],wh[1]);
                            if (typeof th.childNodes[0] == "undefined") { return document.createElement("div"); }
                            return getBoardCell(wh[0],wh[1]);
                        }
                    },
                    // styling for cells
                    style: function(props) {
                        if (arr=="each") {
                            for (var st in props) {
                                for (var r=0; r<size[0]; r++) {
                                    for (var c=0; c<size[1]; c++) {
                                        getBoardCell(r,c).style[st] = props[st];
                                    }
                                }
                            }
                        }
                        else if (typeof arr[0] == "number") {
                            if (arr[0]<0||arr[1]<0||arr[0]>size[0]-1||arr[1]>size[1]-1) { return "OOB"; }
                            for (var st in props) {
                                getBoardCell(arr[0],arr[1]).style[st] = props[st];
                            }
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            for (var st in props) {
                                th.style[st] = props[st];
                            }
                        }
                    },
                    // place cloned piece in cell
                    place: function(piece) {
                        if (arr=="each") {
                            for (var r=0; r<size[0]; r++) {
                                for (var c=0; c<size[1]; c++) {
                                    var th = getBoardCell(r,c);
                                    while (th.firstChild) { th.removeChild(th.firstChild); }
                                    var ra = Math.floor((Math.random() * 3000) + 1);
                                    var n = piece.cloneNode(true);
                                    n.className = "piece pieceID_" + ra;
                                    th.appendChild(n);
                                }
                            }
                        }
                        else if (typeof arr[0] == "number") {
                            var th = getBoardCell(arr[0],arr[1]);
                            while (th.firstChild) { th.removeChild(th.firstChild); }
                            getBoardCell(arr[0],arr[1]).appendChild(piece);
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            while (th.firstChild) { th.removeChild(th.firstChild); }
                            getBoardCell(wh[0],wh[1]).appendChild(piece);
                        }
                    },
                    // remove all pieces from cell
                    rid: function(piece) {
                        if (arr=="each") {
                            for (var r=0; r<size[0]; r++) {
                                for (var c=0; c<size[1]; c++) {
                                    var th = getBoardCell(r,c);
                                    while (th.firstChild) { th.removeChild(th.firstChild); }
                                }
                            }
                        }
                        else if (typeof arr[0] == "number") {
                            var th = getBoardCell(arr[0],arr[1]);
                            while (th.firstChild) { th.removeChild(th.firstChild); }
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            while (th.firstChild) { th.removeChild(th.firstChild); }
                        }
                    },
                    // event listener for cells
                    on: function(ev,func) {
                        if (arr=="each") {
                            for (var r=0; r<size[0]; r++) {
                                for (var c=0; c<size[1]; c++) {
                                    getBoardCell(r,c).addEventListener(ev, func);
                                }
                            }
                        }
                        else if (typeof arr[0] == "number") {
                            if (arr[0]<0||arr[1]<0||arr[0]>size[0]-1||arr[1]>size[1]-1) { return "OOB"; }
                            getBoardCell(arr[0],arr[1]).addEventListener(ev, func);
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            th.addEventListener(ev, func);
                        }
                    },
                    // remove event listener for cells
                    removeOn: function(ev,func) {
                        if (arr=="each") {
                            for (var r=0; r<size[0]; r++) {
                                for (var c=0; c<size[1]; c++) {
                                    getBoardCell(r,c).removeEventListener(ev, func);
                                }
                            }
                        }
                        else if (typeof arr[0] == "number") {
                            if (arr[0]<0||arr[1]<0||arr[0]>size[0]-1||arr[1]>size[1]-1) { return "OOB"; }
                            getBoardCell(arr[0],arr[1]).removeEventListener(ev, func);
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            th.removeEventListener(ev, func);
                        }
                    },
                    // get content of given cell
                    // this is why text property of a piece is required
                    // otherwise it would return null
                    get: function() {
                        if (typeof arr[0] == "number") {
                            if (arr[0]<0||arr[1]<0||arr[0]>size[0]-1||arr[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(arr[0],arr[1]);
                            if (typeof th.childNodes[0] == "undefined") { return null; }
                            // need data because it returns object
                            else { return th.childNodes[0].childNodes[0].data; }
                        }
                        else {
                            var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                            if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                            var th = getBoardCell(wh[0],wh[1]);
                            if (typeof th.childNodes[0] == "undefined") { return null; }
                            else { return th.childNodes[0].childNodes[0].data; }
                        }
                    },
                    // get where in matrix current cell is
                    where: function() {
                        var wh = getObjFromDataAtr(arr.attributes["data-matrixval"].value);
                        if (wh[0]<0||wh[1]<0||wh[0]>size[0]-1||wh[1]>size[1]-1) { return "OOB"; }
                        return [wh[0],wh[1]];
                    }
                };
                return cellMethods;
            }

        };

        return methods;

    }

    function Piece(node) {

        var node = node;

        var methods = {
            clone: function(type="default") {
                var nn = node.cloneNode(true);
                var ra = Math.floor((Math.random() * 3000) + 1);
                if(type=="default"){
                    nn.className = nn.className + " w-16 h-16 rounded-md pieceID_" + ra;
                    if(nn.className.includes("path")){
                        nn.className = nn.className + " popUpPath";
                    }
                }else{
                    nn.className = "w-16 h-16 rounded-md final-path popUpWall pieceID_" + ra;
                }
                return nn;
            },
            style: function(props) {
                for (var st in props) {
                    node.style[st] = props[st];
                }
            }
        };

        return methods;

    }

    // methods to create new game board and pieces
    var methods = {

        // create new game board
        board: function(props) {
            var size = [];
            for (var el in props) {
                if (el=="size") {
                    if (!props.attach) { console.log("Need attachment for game board"); }
                    else {
                        var s = props[el].split("x");
                        var attachedBoard = document.getElementById(props.attach);

                        size.push(parseInt(s[0]),parseInt(s[1]));
                        // create table data to represent game board in DOM
                        for (var i=0; i<size[0]; i++) {
                            var a = document.createElement("tr");
                            a.className = "flex gap-2 boardRow_"+i;
                            for (var k=0; k<size[1]; k++) {
                                var t = document.createElement("td");
                                t.className = 'boardCol_'+k;
                                t.dataset.matrixval = i+"x"+k;
                                a.appendChild(t);
                            }
                            attachedBoard.appendChild(a);
                        }

                        // create checkerboard pattern
                        if (props.style && props.style=="checkerboard") {
                            var colour = "gray";
                            if (props.stylePattern) {
                                for (var i=0; i<attachedBoard.getElementsByTagName("td").length; i++) {
                                    attachedBoard.getElementsByTagName("td")[i].style.background = props.stylePattern[0];
                                }
                                colour = props.stylePattern[1];
                            }

                            for (var r=0; r<size[0]; r++) {
                                if (r%2) var skipCol = true;
                                else var skipCol = false;
                                for (var c=0; c<size[1]; c++) {
                                    if (skipCol)
                                        attachedBoard.getElementsByClassName("boardRow_"+r)[0].childNodes[c].style.background = colour;
                                    skipCol = !skipCol;
                                }
                            }
                        }
                    }
                }
            }
            return Board(attachedBoard,size,props.attach);
        },

        // create new game piece
        piece: function(props) {
            // create new DOM node to serve as piece
            var a = document.createElement("div");
            a.className = props.text;
            return Piece(a);
        }

    };

    return methods;

}());
