// use unique class names to prevent clashing with anything else on the page
// and simplify selectors
// var CSS = {
//   alpha: 'alpha-d2270',
//   black: 'black-3c85d',
//   board: 'board-b72b1',
//   chessboard: 'chessboard-63f37',
//   clearfix: 'clearfix-7da63',
//   highlight1: 'highlight1-32417',
//   highlight2: 'highlight2-9c5d2',
//   notation: 'notation-322f9',
//   numeric: 'numeric-fc462',
//   piece: 'piece-417db',
//   row: 'row-5277c',
//   sparePieces: 'spare-pieces-7492f',
//   sparePiecesBottom: 'spare-pieces-bottom-ae20f',
//   sparePiecesTop: 'spare-pieces-top-4028b',
//   square: 'square-55d63',
//   white: 'white-1e1d7'
// };

var chichess = new Vue({
  el: '#chichess',
  data: {
    pics: {
      "h0": "../static/img/chesspieces/h1.svg",
      "h1": "../static/img/chesspieces/h1.svg",
      "R0": "../static/img/chesspieces/r0.svg",
      "R1": "../static/img/chesspieces/r0.svg", 
      "G": "../static/img/chesspieces/g0.svg",
      "S3": "../static/img/chesspieces/s0.svg",
      "S2": "../static/img/chesspieces/s0.svg",
      "S1": "../static/img/chesspieces/s0.svg", 
      "S0": "../static/img/chesspieces/s0.svg",
      "S4": "../static/img/chesspieces/s0.svg",
      "a1": "../static/img/chesspieces/a1.svg",
      "a0": "../static/img/chesspieces/a1.svg", 
      "s0": "../static/img/chesspieces/s1.svg",
      "c1": "../static/img/chesspieces/c1.svg",
      "c0": "../static/img/chesspieces/c1.svg",
      "e1": "../static/img/chesspieces/e1.svg", 
      "e0": "../static/img/chesspieces/e1.svg",
      "r0": "../static/img/chesspieces/r1.svg",
      "r1": "../static/img/chesspieces/r1.svg",
      "g": "../static/img/chesspieces/g1.svg", 
      "s3": "../static/img/chesspieces/s1.svg",
      "s2": "../static/img/chesspieces/s1.svg",
      "H0": "../static/img/chesspieces/h0.svg",
      "H1": "../static/img/chesspieces/h0.svg", 
      "s4": "../static/img/chesspieces/s1.svg",
      "A1": "../static/img/chesspieces/a0.svg",
      "A0": "../static/img/chesspieces/a0.svg",
      "C1": "../static/img/chesspieces/c0.svg", 
      "C0": "../static/img/chesspieces/c0.svg",
      "E1": "../static/img/chesspieces/e0.svg",
      "E0": "../static/img/chesspieces/e0.svg",
      "s1": "../static/img/chesspieces/s1.svg",
    },
    message: "Hello Chess",
    ROW: [0,1,2,3,4,5,6,7,8,9],
    COL: [0,1,2,3,4,5,6,7,8],
    pos: {
      "h0": [9, 1], "h1": [9, 7], "R0": [6, 0], "R1": [0, 8], 
      "G": [0, 4], "S3": [3, 6], "S2": [3, 4], "S1": [3, 2], 
      "S0": [5, 1], "S4": [3, 8], "a1": [9, 5], "a0": [9, 3], 
      "s0": [-1, -1], "c1": [7, 7], "c0": [7, 1], "e1": [9, 6], 
      "e0": [9, 2], "r0": [9, 0], "r1": [9, 8], "g": [9, 4], 
      "s3": [6, 6], "s2": [6, 4], "H0": [2, 2], "H1": [0, 7], 
      "s4": [6, 8], "A1": [0, 5], "A0": [0, 3], "C1": [2, 7], 
      "C0": [2, 1], "E1": [0, 6], "E0": [0, 2], "s1": [6, 2]
    }
  },
  computed: {
    map: function () {
      temp = {};
      for (var p in this.pos) {
        temp[(this.pos[p][0]*10 + this.pos[p][1]).toString()] = p
      }
      return temp
    }
  }
})
