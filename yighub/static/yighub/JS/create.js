var dropZone=document.getElementById("drop_zone");
var fileInput=document.getElementsByClassName("fileInput");

function add_thumbnail() {
    thumbnails = document.getElementById("upload_thumbnails");
    new_thumbnail = document.createElement("input");
    new_thumbnail.setAttribute("type", "file");
    new_thumbnail.setAttribute("name", "thumbnails");
    thumbnails.appendChild(new_thumbnail);

    new_line = document.createElement("br");
    thumbnails.appendChild(new_line);
};

function add_file() {
    files = document.getElementById("upload_files");
    new_file = document.createElement("input");
    new_div = document.createElement("div");
    new_a = document.createElement("a");

    new_div.className="file";
    new_file.setAttribute("type", "file");
    new_file.setAttribute("name", "files");
    new_file.className="fileInput";
    new_a.className="delete";
    new_a.innerHTML="(이 파일 삭제)";

    files.appendChild(new_div);
    new_div.appendChild(new_file);
    new_div.appendChild(new_a);
};

$(document).on('click', '.delete', function()
{
$(this).parents('.file').remove();
});

function dropHandler(evt) {
  evt.preventDefault();
  for(var i=0; i< fileInput.length; i++){
      if(fileInput[i].files.length==0){
          fileInput[i].files=evt.dataTransfer.files;
          break;
      }
  }
  // Pass event to removeDragData for cleanup
  removeDragData(evt);
  add_file();
};

function dragOverHandler(ev) {
  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
};

function removeDragData(ev) {
  console.log('Removing drag data');

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to remove the drag data
    ev.dataTransfer.items.clear();
  } else {
    // Use DataTransfer interface to remove the drag data
    ev.dataTransfer.clearData();
  }
};

function add_photos() {
			photos = document.getElementById("upload_photos");
			size = Number(document.getElementById("size").value);

			hr = document.createElement("hr");
			photos.appendChild(hr);

			new_photo = document.createElement("div");
			new_photo.setAttribute("class", "container-fluid upload-photo");

			photo_label = document.createElement("label");
			photo_label.innerHTML = "사진";
			new_photo.appendChild(photo_label);

			input = document.createElement("input");
			input.type = "file";
			input.name = "photo_" + size;
			new_photo.appendChild(input);

			br1 = document.createElement("br");
			new_photo.appendChild(br1);
			br2 = document.createElement("br");
			new_photo.appendChild(br2);


			description_label = document.createElement("label");
			description_label.innerHTML = "설명";
			new_photo.appendChild(description_label);

			textarea = document.createElement("textarea");
			textarea.name = "description_" + size;
			textarea.rows = 5;
			textarea.placeholder = "사진 설명을 해주세요";
			textarea.style.width="100%";
			new_photo.appendChild(textarea);

			photos.appendChild(new_photo);

			document.getElementById("size").value = size + 1;
		}
