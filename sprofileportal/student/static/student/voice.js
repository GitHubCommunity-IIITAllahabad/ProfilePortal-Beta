function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

      var recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.lang = "en-IN";
      recognition.start();
      
      recognition.onresult = function(e) {
        var speech1 = (e.results[0][0].transcript).trim();
        var speech2 = "";
        for(i=0;i<speech1.length;i++)
        {
          if(speech1[i]!=" ")
          {
            speech2+=speech1[i].toUpperCase();
          }
        }
        document.getElementById('q').value
                                 = speech2;
        recognition.stop();
        document.getElementById('searchbtn').click();
      };

      recognition.onerror = function(e) {
        recognition.stop();
      }

    }
  }
