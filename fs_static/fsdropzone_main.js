Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#my-dropzone',{
    //url:'/fileserver/upload/',
    maxFiles:20,          
    maxFilesize:4,      //mb
    addRemoveLinks: true,
    dictRemoveFile : "X",
    dictDefaultMessage: "<font style='font-size:11px'>해당 영역을 클릭하거나, 파일을 드래그하여 넣으면 업로드 진행 됩니다.</font>",
    acceptedFiles:'.png,.jpg,.txt,.log',
    init: function() {
        this.on('accept', function(file, done) {
            console.log(file);
            if ( file.name.substr(filename.length-3, 3)!="log" ) {
                done("*.log 파일만 업로드 가능합니다");
            } else {
                done();
            }
        });

        this.on('addedfile', function(file) {
            console.log("Dropzone#addedfile event")
            //console.log(file)
            //x = confirm('화면에서 제거하시겠습니까?\n(여기서 지운다고 서버의 파일이 삭제되는 것은 아닙니다)');
            //if(!x)  return false;
        });


        this.on('removedfile', function(file, errorMessage) {
            //x = confirm('화면에서 제거하시겠습니까?\n(여기서 지운다고 서버의 파일이 삭제되는 것은 아닙니다)');
            //if(!x)  return false;
        });

        this.on("success", function(response) {
            // 성공할 경우 response는 file객체가 전달됨.
            console.log("#onsuccess")
            if ( document.getElementById('filelist') )
            {
                document.getElementById('filelist').contentWindow.location.reload();
            }
            //console.log(response.status)
            //console.log(response)
        });

        this.on('error', function(file, response) {
            console.log("#error")
            console.log(response)
            if(response.msg)
                errorMessage = response.msg
            else
                errorMessage = response
            
            //#errorDisplay[errorDisplay.length - 1].innerHTML = errorMessage;
            file.previewElement.querySelectorAll('.dz-error-message span')[0].textContent = errorMessage;
            /*
            if (errorMessage.indexOf('Error 404') !== -1) {
                errorDisplay[errorDisplay.length - 1].innerHTML = 'Error 404: The upload page was not found on the server';
            }
            */
        });
    }
})

