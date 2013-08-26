ig.module(
	'game.entities.levelproblem'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLevelproblem = EntityLevel.extend({
    name: 'Problem',
	correct: false,
	
	/******* callbacks *******/
	
	onSubmit: function(success, message){
		if(success == 1){
			//this.correct=true;						
			//$("#prob_submit_msg").html('<div class="alert">'+'Correct!'+'</div>');
			ig.gm.problemStates[ig.gm.currentProblem].solved=true;
            if(ig.gm.category != '')
            {
                if(EQUIPMENT[GALAXYPROBLEMS[ig.gm.category].equipment] < 4)
                    EQUIPMENT[GALAXYPROBLEMS[ig.gm.category].equipment]++;
            }
			ig.gm.ProblemHide();
			if (this.endingCheck() && !ig.gm.endingFlag)
            {
                ig.gm.loadLevel("Ending",true);
                ig.gm.endingFlag = true;
            }
            else ig.gm.loadLevel(ig.gm.previousLevelName, true);
            ig.sm.play('problem Solved');
		}
		else if(success == 0){
            if(message == "You have already solved this problem!")
            {

                var prob_sub_msg = $('#prob_submit_msg');
                prob_sub_msg.hide().html('<div class="alert alert-error">' + message + '</div>').slideDown('normal');
                setTimeout(function () {
                    prob_sub_msg.slideUp('normal', function () {
                        prob_sub_msg.html('').show();
                    });
                    ig.gm.problemStates[ig.gm.currentProblem].solved=true;
                    ig.gm.ProblemHide();
                    ig.gm.loadLevel(ig.gm.previousLevelName, true);
                }, 2000);
            }
            else
            {
                var prob_sub_msg = $('#prob_submit_msg');
                prob_sub_msg.hide().html('<div class="alert alert-error">' + message + '</div>').slideDown('normal');
                setTimeout(function () {
                    prob_sub_msg.slideUp('normal', function () {
                        prob_sub_msg.html('').show();
                    });
                }, 3000);
            }
		}
	},
	
	onTrigger: function(trigger,other){
		this.parent(trigger,other);
	},
	
	onUI: function(name){
		if(name=='return'){
			ig.gm.ProblemHide();
			ig.gm.loadLevel(ig.gm.previousLevelName, true);
		}
		
		// FIXME: will lose focus (next time need to click twice)
		if(name=='hint'){
			hintdiv = $("#problemhintdialog");
			hintdiv.dialog().dialog("open");
			hintdiv.html(getProblemHint(PROBLEMS[ig.gm.currentProblem].PID));
		}
		
		// for debug convenience: solve button
		if(name=='solve'){
			this.onSubmit(1);
		}
	},

	
	/******* events *******/	
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		ig.problem = this;
        if(typeof ig.gm!='undefined')
			ig.gm.ProblemDisplay();
	},
	
	update: function(){
		this.parent();
	},

    endingCheck: function(){
        var endingSwitch = true;
        for (var i in ig.gm.problemStates)
        {
            problemID = Math.floor(i.slice(0,1));
            if(!ig.gm.problemStates[i].solved && problemID > 1 && problemID < 10 )
            {
                endingSwitch = false;
                break;
            }
        }
        return endingSwitch;
    }
	
	
});

});