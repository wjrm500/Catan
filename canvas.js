const nodes_arr = [[4.5, 6.5], [3, 5, 6, 8], [1.5, 3.5, 4.5, 6.5, 7.5, 9.5], [0, 2, 3, 5, 6, 8, 9, 11], [0.5, 1.5, 3.5, 4.5, 6.5, 7.5, 9.5, 10.5], [0, 2, 3, 5, 6, 8, 9, 11], [0.5, 1.5, 3.5, 4.5, 
    6.5, 7.5, 9.5, 10.5], [0, 2, 3, 5, 6, 8, 9, 11], [0.5, 1.5, 3.5, 4.5, 6.5, 7.5, 9.5, 10.5], [0, 2, 3, 5, 6, 8, 9, 11], [0.5, 1.5, 3.5, 4.5, 6.5, 7.5, 9.5, 10.5], [0, 2, 3, 5, 6, 8, 9, 11], [1.5, 3.5, 4.5, 6.5, 7.5, 9.5], [3, 5, 6, 8], [4.5, 6.5]];
setTimeout(function() {
    debugger;
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    ctx.fillStyle = '#000000';
    for (let i = 0; i < nodes_arr.length; i++) {
        let nodes = nodes_arr[i];
        for (let node of nodes) {
            ctx.beginPath();
            ctx.arc(node * 5, i * 5, 1, 0, 2 * Math.PI, false);
            ctx.fill();
            ctx.lineWidth = 1;
            ctx.strokeStyle = '#000000';
            ctx.stroke();
        }
    }
}, 200);