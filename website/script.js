function changeIndex(index, direction) {
    const maxIndex = 3;
    const minIndex = 0;

    if (direction === "right") {
        index = index < maxIndex ? index + 1 : minIndex;
    } else if (direction === "left") {
        index = index > minIndex ? index - 1 : maxIndex;
    }

    return index;
}

function updateImages() {
  title.textContent = days[index].name;
  mackinaw.src = days[index].mackinaw;
  full.src = days[index].full;
  detroit.src = days[index].detroit;
  document.getElementById("description").textContent = days[index].description;
}

let index = 0;

const title = document.getElementById("title");
const desc = document.getElementById("description");
const left = document.getElementById("left-arrow");
const right = document.getElementById("right-arrow");
const full = document.getElementById("full");
const mackinaw = document.getElementById("mackinaw");
const detroit = document.getElementById("detroit");

const days = [
  { name: " Day Zero",
    full: "images/0_full.png",
    mackinaw: "images/0_mackinaw.png",
    detroit: "images/0_detroit.png",
    description: "This is the initial day. To the left is an image of the graph zoomed in on northern Michigan, and to the right is an image of the graph zoomed in on Detroit and Canada." },
              
  { name: " Day One ",
    full: "images/1_full.png",
    mackinaw: "images/1_mackinaw.png",
    detroit: "images/1_detroit.png",
    description: "As you can see, the overall ice concentration goes down from the initial day. It remains the same in some areas such as the area around the St. Mary's River." },
              
  { name: " Day Two ",
    full: "images/2_full.png",
    mackinaw: "images/2_mackinaw.png",
    detroit: "images/2_detroit.png",
    description: "The ice concentration continues to decrease. It still stays about the same around the St. Mary's River." },
              
  { name: "Day Three",
    full: "images/3_full.png",
    mackinaw: "images/3_mackinaw.png",
    detroit: "images/3_detroit.png",
    description: "The overall trend of ice concenration decreasing continues, and the areas with high concentration remain the same." }
];


left.onclick = function() {
  index = changeIndex(index, "left")
  title.textContent = days[index].name;
  desc.textContent = days[index].name;
  updateImages();
  
  
};

right.onclick = function() {
  index = changeIndex(index, "right")
  title.textContent = days[index].name;
  desc.textContent = days[index].name;
  updateImages();
};
