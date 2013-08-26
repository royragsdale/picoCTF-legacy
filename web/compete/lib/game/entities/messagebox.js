ig.module(
	'game.entities.messagebox'
)
.requires(
	'game.entities.ui'
)
.defines(function(){

EntityMessagebox = EntityUi.extend({
	name: 'messagebox',
	animSheet: new ig.AnimationSheet('media/messagebox.png',271,113),	
	size: {x:271, y:113},
	textOffset: {x:10, y:10},
	displayWidth: 200,
	text: '',
	displayText: '',
	currentLine: '',
	textIndex: 0,
	font: null,
	enabled: true,
	finished: true,
	
	
	/******* functions *******/
	
	setWhat: function(what){
		this.text=what;
		this.displayText='';
		this.currentLine='';
		this.textIndex=0;
		this.finished=false;		
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( 280, 224, settings );
		
		this.addAnim('background', 1, [0]);
		
		if(typeof ig.gm!='undefined'){
			this.font=ig.gm.fonts[0];
			this.enabled=false;
			this.currentAnim=this.anims['background'];
		}
	},
		
	update: function(){		
		if(!this.enabled)return;
		this.parent();
		
		if(this.textIndex<this.text.length){
			var ch=this.text[this.textIndex];
			this.currentLine+=ch
			this.displayText+=ch
			
			// break new line
			if(ch==' '){
				if(this.font.widthForString(this.currentLine)>this.displayWidth){
					ch='\n';
					this.displayText+='\n';
				}			
			}
			
			if(ch=='\n')
				this.currentLine='';
			// a new char
			this.textIndex++;
		}else{
			this.finished=true;
		}				
	},	
	
	draw: function(){
		if(!this.enabled)return;				
		this.parent();
		if(typeof ig.gm!='undefined'){
			// should draw on screen coord
			this.font.draw(this.displayText,
					   this.pos.x-ig.game.screen.x+this.textOffset.x,
					   this.pos.y-ig.game.screen.y+this.textOffset.y,
					   ig.Font.ALIGN.LEFT);				
		}
	}
});

});