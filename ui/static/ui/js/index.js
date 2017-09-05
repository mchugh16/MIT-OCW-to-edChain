var Api = {
	"postStuffNoData": function(config){
		return $.ajax({
			"method": config.method,
			"url": config.url
		});
	},	
};

$(document).ready(function(){

	var courseCardTemplate = $("#course-card-li-template").html();
 	
	var refreshDiscoverCourses = function refreshDiscoverCourses(){
		Api.postStuffNoData({
			"method" : "get",
			"url" : "/api/discovercourses"
		}).success(function(data){
			var rendered = Mustache.render(courseCardTemplate, courses.posts);
			$('.discoverCourses').html(rendered);
		});
	};
	refreshDiscoverCourses();
});
