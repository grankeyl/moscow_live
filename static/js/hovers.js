// hover element add class active
$('.verify').hover(
	function () {
		$(this).closest('.verify_mark').find('.verify_mark_block').addClass('active')
	},
	function () {
		$(this).closest('.verify_mark').find('.verify_mark_block').removeClass('active')
	},
)