ig.module(
    'game.classes.soundmanager'
)
.requires(
    'impact.sound'
)
.defines(function(){

SoundManager = ig.Class.extend({
	disabled: false,
	sounds : {},	
	destvolume:1,
	mute:false,
	
	soundList: {
		'select': 'media/sound/select.*',
		'click': 'media/sound/click.*',
        'robot_hull_knock': 'media/sound/robot_hull_knock.*',
        'robot_jump': 'media/sound/robotjump.*',
        //'robot_confuse':'media/sound/robot_confuse.*',
        'problem Solved':'media/sound/problem_Solved.*',
        'car_driving': 'media/sound/Car_Driving.*',
        'daydream': 'media/sound/Toast_Daydream.*',
        'crash': 'media/sound/CrashLand.*',
        'hologram_pulsa': 'media/sound/Hologram.*',
        'hologram_speak': 'media/sound/Hologram_speak.*',
        'hologram_pulsa_end': 'media/sound/Hologram_fade.*',
        'spaceship': 'media/sound/spaceship.*'
	},
	
	switchMute: function(){
		if(ig.soundManager.volume>0){
			ig.soundManager.volume=0;
			this.mute=true;
		}else{
			ig.soundManager.volume=0.75;
			this.mute=false
		}
		return this.mute;
	},
	
	play: function(s){
		if(this.disabled)return;
		if(s in this.sounds){
			this.sounds[s].play();
		}else{
			// TODO: sound not found
		}
	},
	
	playbgm: function(s){
	},

	
	/******* events *******/

	init: function(){
		ig.sm=this;
		if(this.disabled)return;

		for(s in this.soundList){
			this.sounds[s]=new ig.Sound(this.soundList[s]);
		}	
	},
	
	update: function(){
	},
	
});

})