onLoad();

function onLoad() {
	$.get("json/config.json", function(json) {
		json.reverse().forEach(data => {
			var element = createLinkElement(data["name"], data["url"]);
			$(".layout").prepend(element);
		});
	}, "json");
}

function createLinkElement(name, url) {
	var result = document.createElement("A");
	result.href = url
	result.innerHTML = "<DIV class=\"link\">" + name + "</DIV>";
	return result;
}