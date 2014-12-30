if (!RedactorPlugins) var RedactorPlugins = {};
 
RedactorPlugins.spoiler = function()
{
	return {
		init: function()
		{
			var button = this.button.addAfter('deleted', 'spoiler', '스포일러');
			this.button.setAwesome('spoiler', 'fa-exclamation-triangle');
 
			this.button.addCallback(button, this.spoiler.set);
			this.observe.addButton('span.spoiler', 'spoiler');
		},
		set: function()
		{
			this.inline.toggleClass('spoiler');
		}
	};
};
