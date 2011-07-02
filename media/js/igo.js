function touch(x, y) {
  $('#touch_x').val(x);
  $('#touch_y').val(y);
  $('#touchform').submit();
  return false;
}
