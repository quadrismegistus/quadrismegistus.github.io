// using d3 for convenience
var main = d3.select("main");
var scrolly = main.select("#scrolly");
var figure = scrolly.select("figure");
var article = scrolly.select("article");
var step = article.selectAll(".step");

// initialize the scrollama
var scroller = scrollama();

// generic window resize listener event
function handleResize() {
  // 1. update height of step elements
  // var stepH = Math.floor(window.innerHeight * 0.75);
  // step.style("height", stepH + "px");

  var figureHeight = window.innerHeight / 2;
  var figureMarginTop = (window.innerHeight - figureHeight) / 2;

  figure
    .style("height", figureHeight + "px")
    .style("top", figureMarginTop + "px");

  // 3. tell scrollama to update new element dimensions
  scroller.resize();
}

function pad(num, size){ return ('000000000' + num).substr(-size); }

function preload_images(num_slides) {
  var images=[]
  SLIDES.forEach(function(imgsrc,i) {
    image=new Image
    image.src = imgsrc
    images.push(image)
    console.log('loaded image: '+imgsrc)
  })
  return images
}


// scrollama event handlers
function handleStepEnter(response) {
  console.log(response);
  // response = { element, direction, index }

  // add color to current step only
  step.classed("is-active", function(d, i) {
    return i === response.index;
  });

  // update graphic based on step
  //figure.select("p").text(response.index + 1);
	index_int = parseInt(response.index) + 1
  index_i = parseInt(response.index)
	index_str = pad(index_int, 3)
	// imgcode='<img src="slides/Slide' + index_str + '.png" />'
  imgsrc=SLIDES[index_i]
  // imgcode='<img src="' + SLIDES[index_i] +'" width="720" />'
  imgcode=`<a class='popup-link' href='${imgsrc}' target='_blank' border="0" style="border:0"><img src='${imgsrc}' width="720" /></a>`
	console.log(imgcode)
	figure.select("p").html(imgcode)
  
}

function setupStickyfill() {
  d3.selectAll(".sticky").each(function() {
    Stickyfill.add(this);
  });
}

function init() {

  setupStickyfill();

  // 1. force a resize on load to ensure proper dimensions are sent to scrollama
  handleResize();

  // 2. setup the scroller passing options
  // 		this will also initialize trigger observations
  // 3. bind scrollama event handlers (this can be chained like below)
  scroller
    .setup({
      step: "#scrolly article .step",
      offset: 0.33,
      debug: false
    })
    .onStepEnter(handleStepEnter);

  // setup resize event
  window.addEventListener("resize", handleResize);

  // preload
  preload_images(59);
}

// kick things off
init();

