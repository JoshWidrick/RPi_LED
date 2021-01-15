function panelChecker(checkbox, item_id) {
  var divx = document.getElementById(item_id);

  // If the checkbox is checked, display the output text
  if (checkbox.checked == true){
    divx.style.borderColor = "#00FFFF";
  } else {
    divx.style.borderColor = "#000000";
  }
}