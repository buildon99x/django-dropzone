//ex) <iframe id="filelist" src="/fs/list/" width="800px" height="200px" frameborder="0" onload="resizeIframe(this);"></iframe>
function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
}