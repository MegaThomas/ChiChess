var ws = new WebSocket('ws://localhost:5000/websocket')

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
    status: "Hello Chess!",
    ROW: [0,1,2,3,4,5,6,7,8,9],
    COL: [0,1,2,3,4,5,6,7,8],
    pos: {},
    selectPiece: null,
    selectStep: false
  },
  computed: {
    map: function () {
      temp = {};
      for (var p in this.pos) {
        temp[(this.pos[p][0]*10 + this.pos[p][1]).toString()] = p
      }
      return temp
    }
  },
  methods: {
    onClickPiece: function (e) {
      if (this.selectStep) {
        this.selectStep = false;
        var vm = this;
        ws.send(
          '/move?o=' + this.selectPiece + 
          '&n=' + e.currentTarget.id.slice(-2));
      } else {
        if (e.currentTarget.childElementCount == 2) {
          this.selectStep = true;
          this.selectPiece = e.currentTarget.id.slice(-2);
          e.currentTarget.className += " selected-chi";
        }
      }
    },
    onClickRestart: function () {
      var vm = this;
      axios.get('/restart')
        .then(function (response) {
          console.log(response);
          vm.pos = response.data;
          vm.status = "";
        })
        .catch(function (error) {
          console.log(error);
        })
    }
  },
  created() {
    vm = this;
    ws.onmessage = function(response) {
      if (response.data == "illegal") {
        vm.status = "Illegal Move";
      } else {
        vm.pos = JSON.parse(response.data);
        vm.status = "";
      }
      document.getElementById('sq-' + vm.selectPiece).classList.remove("selected-chi");
    };
  }
})
