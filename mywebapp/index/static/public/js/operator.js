
// 设置画布初始属性
const canvasMain = document.querySelector('.canvasMain');
const canvas = document.getElementById('canvas');
const resultGroup = document.querySelector('.resultGroup');

// 设置画布宽高背景色
canvas.width = canvas.clientWidth;
canvas.height = canvas.clientHeight;
canvas.style.background = "#8c919c";

const annotate = new LabelImage({
	canvas: canvas,
	scaleCanvas: document.querySelector('.scaleCanvas'),
	scalePanel: document.querySelector('.scalePanel'),
	annotateState: document.querySelector('.annotateState'),
	canvasMain: canvasMain,
	resultGroup: resultGroup,
	crossLine: document.querySelector('.crossLine'),
	labelShower: document.querySelector('.labelShower'),
	screenShot: document.querySelector('.screenShot'),
	screenFull: document.querySelector('.screenFull'),
	colorHex: document.querySelector('#colorHex'),
	toolTagsManager: document.querySelector('.toolTagsManager'),
	historyGroup: document.querySelector('.historyGroup')
});

// 初始化交互操作节点
const prevBtn = document.querySelector('.pagePrev');                    // 上一张
const nextBtn = document.querySelector('.pageNext');                    // 下一张
const taskName = document.querySelector('.pageName');                   // 标注任务名称
const processIndex = document.querySelector('.processIndex');           // 当前标注进度
const processSum = document.querySelector('.processSum');               // 当前标注任务总数

let imgFiles = [];    //选择上传的文件数据集
let imgIndex = 1;       //标定图片默认下标;
let imgSum = 10;        // 选择图片总数;

// 初始化图片状态
function initImage(path) {
	for(var i = 0;i< path.length;i++)
	{
		imgFiles.push(path[i]);
	}
	//imgFiles.append()
	if(imgFiles.length > 0){
		selectImage(0);
	}
	else{
		alert("请选择要打开的文件夹")
	}
	processSum.innerText = imgFiles.length;
}

//切换操作选项卡
let tool = document.getElementById('tools');
tool.addEventListener('click', function(e) {
	for (let i=0; i<tool.children.length; i++) {
		tool.children[i].classList.remove('focus');
	}
	e.target.classList.add('focus');
	switch(true) {
		case e.target.className.indexOf('toolDrag') > -1:  // 拖拽
			annotate.SetFeatures('dragOn', true);
			break;
		case e.target.className.indexOf('toolRect') > -1:  // 矩形
			annotate.SetFeatures('rectOn', true);
			break;
		case e.target.className.indexOf('toolTagsManager') > -1:  // 标签管理工具
			annotate.SetFeatures('tagsOn', true);
			break;
		default:
			break;
	}
});

// 获取下一张图片
nextBtn.onclick = function() {
	annotate.Arrays.imageAnnotateMemory.length > 0 && localStorage.setItem(taskName.textContent, JSON.stringify(annotate.Arrays.imageAnnotateMemory));  // 保存已标定的图片信息
	if (imgIndex >= imgFiles.length) {
		imgIndex = 1;
		selectImage(0);
	}
	else {
		imgIndex++;
		selectImage(imgIndex - 1);
	}
};

// 获取上一张图片
prevBtn.onclick = function() {
	annotate.Arrays.imageAnnotateMemory.length > 0 && localStorage.setItem(taskName.textContent, JSON.stringify(annotate.Arrays.imageAnnotateMemory));  // 保存已标定的图片信息
	if (imgIndex === 1) {
		imgIndex = 1;
		selectImage(0);
	}
	else {
		imgIndex--;
		selectImage(imgIndex - 1);
	}
};

document.querySelector('.openFolder').addEventListener('click', function() {
	document.querySelector('.openFolderInput').click()
});

function selectImage(index) {
	openBox('#loading', true);
	processIndex.innerText = imgIndex;
	taskName.innerText = imgFiles[index].name || imgFiles[index].split('/')[3];
	let content = localStorage.getItem(taskName.textContent);
	let img = imgFiles[index].name ? window.URL.createObjectURL(imgFiles[index]) : imgFiles[index];
	content ? annotate.SetImage(img, JSON.parse(content)) : annotate.SetImage(img);
}//querySelector('.saveJson')

document.getElementById("saveJson").addEventListener('click', function() {
	annotate.Arrays.imageAnnotateMemory.map((item)=>{
		if(annotate.Arrays.imageAnnotateMemory.length <= 0 )
		alert('当前图片未有有效的标定数据');
		else{
			console.log(item);
			document.getElementById("yMin").value = item.rectMask.yMin;
			document.getElementById("xMin").value = item.rectMask.xMin;
			document.getElementById("height").value = item.rectMask.height;
			document.getElementById("width").value = item.rectMask.width;
			document.getElementById("label").value = item.labels.labelName;
			document.getElementById("pic_num").value = imgIndex
			document.getElementById("pic_url").value = imgFiles[imgIndex]
			document.getElementById("mid").value = document.getElementById("mid").value
		}
	});
});


//弹出框
function openBox (e, isOpen) {
	let el = document.querySelector(e);
	let maskBox = document.querySelector('.mask_box');
	if (isOpen) {
		maskBox.style.display = "block";
		el.style.display = "block";
	}
	else {
		maskBox.style.display = "none";
		el.style.display = "none";
	}
}