

var create_email = false;
var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;

if (!('webkitSpeechRecognition' in window)) {
  upgrade();
  } else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
  };
recognition.onerror = function(event) {
  if (event.error == 'no-speech') {
    showInfo('info_no_speech');
    ignore_onend = true;
  }
  if (event.error == 'audio-capture') {
    showInfo('info_no_microphone');
    ignore_onend = true;
  }
  if (event.error == 'not-allowed') {
    if (event.timeStamp - start_timestamp < 100) {
      showInfo('info_blocked');
    } else {
      showInfo('info_denied');
    }
    ignore_onend = true;
  }
};
recognition.onend = function() {
  recognizing = false;
  if (ignore_onend) {
    return;
  }
  if (!final_transcript) {
    showInfo('info_start');
    return;
  }
  showInfo('');
  if (window.getSelection) {
    window.getSelection().removeAllRanges();
    var range = document.createRange();
    range.selectNode(document.getElementById('oritext'));
    window.getSelection().addRange(range);
  }
  if (create_email) {
    create_email = false;
    createEmail();
  }
};
recognition.onresult = function(event) {
  var interim_transcript = '';
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal) {
      final_transcript += event.results[i][0].transcript;
    } else {
      interim_transcript += event.results[i][0].transcript;
    }
  }
  final_transcript = capitalize(final_transcript);

  if (final_transcript.length>1){
    oritext.value = linebreak(final_transcript);
  }
  else
  {
  oritext.value = linebreak(interim_transcript);
  }
  convert()
  if (final_transcript || interim_transcript) {
    showButtons('inline-block');
  }
};
}
function upgrade() {
start_button.style.visibility = 'hidden';
showInfo('info_upgrade');
}
var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}
var first_char = /\S/;
function capitalize(s) {
return s.replace(first_char, function(m) { return m.toUpperCase(); });
}
function createEmail() {
var n = final_transcript.indexOf('\n');
if (n < 0 || n >= 80) {
  n = 40 + final_transcript.substring(40).indexOf(' ');
}
var subject = encodeURI(final_transcript.substring(0, n));
var body = encodeURI(final_transcript.substring(n + 1));
window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
}
function copyButton() {
if (recognizing) {
  recognizing = false;
  recognition.stop();
}
copy_button.style.display = 'none';
copy_info.style.display = 'inline-block';
showInfo('');
}
function emailButton() {
if (recognizing) {
  create_email = true;
  recognizing = false;
  recognition.stop();
} else {
  createEmail();
}
email_button.style.display = 'none';
email_info.style.display = 'inline-block';
showInfo('');
}
function startButton(event) {
if (recognizing) {
  recognition.stop();
  return;
}

// Recorder.js recorder function start here
// to cut down on number of clicks for permissions
  recorder && recorder.record();
  __log('Recording...');

final_transcript = '';
recognition.lang = dialect;
recognition.start();
ignore_onend = false;
oritext.value = '';

showInfo('info_allow');
showButtons('none');
start_timestamp = event.timeStamp;
}
function showInfo(s) {
if (s) {
  for (var child = info.firstChild; child; child = child.nextSibling) {
    if (child.style) {
      child.style.display = child.id == s ? 'inline' : 'none';
    }
  }
  info.style.visibility = 'visible';
} else {
  info.style.visibility = 'hidden';
}
}
var current_style;
function showButtons(style) {
if (style == current_style) {
  return;
}
current_style = style;
}

// Button Functionality

$('#stop_button').hide();
$('#record-status').hide();
$('#submit-audio').prop('disabled',true);

$('#start_button').click(function() {
  $('#start_button').hide();
  $('#stop_button').show();
  $('#record-status').show();
  recognition.lang = dialect;
  final_transcript = '';
  recognition.start();
});


$('#stop_button').click(function() {
  $('#stop_button').hide();
  $('#start_button').show();
  $('#record-status').hide();
  $ ('#submit-audio').prop('disabled',false);
  stopRecording(this);
  startButton(event);
});
