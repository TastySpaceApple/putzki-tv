var spawn = require('child_process').spawn;
(function(){ 

	exports.on_fingermote = function(callback){
		fingermote_callback = callback;

			var fingermote = spawn('python', ['app/fingermote/main.py']);
			fingermote.stdout.setEncoding('utf8');
			fingermote.stdout.pipe(process.stdout);
			fingermote.stdout.on('data', function(data){
				console.log("out");
				console.log(data);
				callback(data);
			});
	}
})()
