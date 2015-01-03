if (!RedactorPlugins) var RedactorPlugins = {};
 
RedactorPlugins.krfix = function()
{
	return {
		init: function()
		{
			this.$editor.click();
		}
	};
};
