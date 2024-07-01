// click element add class active
$(document).on('click', '.dropdown_item_catalog', function () {
	$('.header_link_dropdown.catalog').toggleClass('active')
	$('.chevron_down.catalog').toggleClass('active')
})

$(document).on('click', '.dropdown_item_rating', function () {
	$('.header_link_dropdown.rating').toggleClass('active')
	$('.chevron_down.rating').toggleClass('active')
})
