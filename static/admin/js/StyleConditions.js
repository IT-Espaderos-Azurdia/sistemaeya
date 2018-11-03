document.addEventListener('DOMContentLoaded',
	function(){
		try{
			SetStyleExpediente();
			SetCheckTenencia();	
		}
		catch{
			SetCheckTenencia();		
		}
	}
, false);


function SetStyleExpediente(){ 

	var Subtitulo = document.getElementById("txtSubtitulo");

	if ( document.getElementById("id_esta_entregado").checked )
	{
		Subtitulo.className = "center red lighten-5 black-text lighten-4 s12 l12";
	}
	else
	{
		Subtitulo.className = "center blue-grey darken-3 s12 l12 white-text";
	}

}

function SetCheckTenencia(){

	var Tenencias = document.getElementById("id_tenencias");	
	if(Tenencias.value == 0)
	{
		SetCheckTenencias(false);
		/*document.getElementById("id_cobro_4").checked = false;*/
	}
	else
	{
		SetCheckTenencias(true);
		/*document.getElementById("id_cobro_4").checked = true;*/
	}

}

function SetCheckTenencias(Valor){

	for(i =0; i<800; i++)
	{
		try{
			if(document.getElementById("id_cobro_"+i).value == 14){
				document.getElementById("id_cobro_"+i).checked = Valor;			
			}
		}
		catch{
			i = 1000;
		}
	}
}