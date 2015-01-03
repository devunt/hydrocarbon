if (!RedactorPlugins) var RedactorPlugins = {};
 
RedactorPlugins.krfix = function()
{
	return {
		init: function()
		{
			console.log(this.$editor);
			this.$editor.click();
		}
	};
};
