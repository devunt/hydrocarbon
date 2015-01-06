if (!RedactorPlugins) var RedactorPlugins = {};
 
RedactorPlugins.autosave_garlic = function()
{
	return {
		init: function()
		{
			this.opts.changeCallback = function()
			{
				this.$textarea.trigger('change');
			}
		}
	};
};
