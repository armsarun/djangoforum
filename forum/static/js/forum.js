$(".avatar,.headeravatar, .recentuseravatar").each(function () {
  var color;
  var letter = $(this).text()
  var a = letter.match(/a/i);
  var b = letter.match(/b/i);
  var c = letter.match(/c/i);
  var d = letter.match(/d/i);
  var e = letter.match(/e/i);
  var f = letter.match(/f/i);
  var g = letter.match(/g/i);
  var h = letter.match(/h/i);
  var i = letter.match(/i/i);
  var j = letter.match(/j/i);
  var k = letter.match(/k/i);
  var l = letter.match(/l/i);
  var m = letter.match(/m/i);
  var n = letter.match(/n/i);
  var o = letter.match(/o/i);
  var p = letter.match(/p/i);
  var q = letter.match(/q/i);
  var r = letter.match(/r/i);
  var s = letter.match(/s/i);
  var t = letter.match(/t/i);
  var u = letter.match(/u/i);
  var v = letter.match(/v/i);
  var w = letter.match(/w/i);
  var x = letter.match(/x/i);
  var y = letter.match(/y/i);
  var z = letter.match(/z/i);

  if (b || e || j || p || v) {
    color = "#B0171F";
    $(this).css("background", color);
  }
  else if (m || f || k || q || w) {
    color = "#9B30FF";
    $(this).css("background", color);
  }
  else if (l || g || r || x) {
    color = "#FFA500";
    $(this).css("background", color);
  }
  else if (t || d || s || y) {
    color = "#757575";
    $(this).css("background", color);
  }
  else if (c || h || n || z) {
    color = "#FFA500";
    $(this).css("background", color);
  }
  else if (a || i || o || u) {
    color = "#FF3030";
    $(this).css("background", color);
  }
  else {
    color = "#1E90FF";
    $(this).css("background", color);
  }
});


// profileedit

function profile_validate() {
  var upload = $('#profile_submit').value
  if (upload !="") {
    var ext = $('#profile_choose').val().split('.').pop().toLowerCase();
    if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
      alert('invalid File!');
    }
  }

}


//profileedit
