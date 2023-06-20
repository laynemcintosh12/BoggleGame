class BoggleGame {
    constructor(boardId, secs = 60) {
      this.secs = secs;
      $(".timer", this.board).text(this.secs);
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId);
      this.timer = setInterval(this.tick.bind(this), 1000);
      $(".guessForm", this.board).on("submit", this.handleSubmit.bind(this));
    }
  

    // handle guess submission
    async handleSubmit(evt) {
      evt.preventDefault();
      const $guess = $(".guess", this.board);
      let guess = $guess.val();
      if (!guess) return;  // no guess
      if (this.words.has(guess)) {
        $(".jsMessage", this.board).text(`Already found ${guess}`);  //already found guess
        return;
      }
      // check server 
      const res = await axios.get("/check-guess", { params: { guess: guess }});
      if (res.data.result === "not-word") {
        $(".jsMessage", this.board).text(`${guess} is not a real word`);
      } 
      else if (res.data.result === "not-on-board") {
        $(".jsMessage", this.board).text(`${guess} is not on this board`);
      } 
      else {
        $(".words", this.board).append($("<li>", { text: guess })); // add right answer to a list under the board
        this.score += guess.length;                                 // make the score = the score plus the length of the word
        $(".score", this.board).text(this.score);                   // display the score
        this.words.add(guess);                                      // add the guess to a JS array so that they cant use answer twice
        $(".jsMessage", this.board).text(`Added: ${guess}`)         // display a message showing it was added
      }
      $guess.val("");
    }
  

    // handle a second passing in game 
    async tick() {
      this.secs -= 1;
      $(".timer", this.board).text(this.secs);
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  

    // score and end game
    async scoreGame() {
      $(".guessForm", this.board).hide();
      const res = await axios.post("/post-score", { score: this.score });
      if (res.data.newHigh) {
        $(".jsMessage", this.board).text(`New Record: ${this.score}`);
      } 
      else {
        $(".jsMessage", this.board).text(`Final Score: ${this.score}`)
      }
    }
  }