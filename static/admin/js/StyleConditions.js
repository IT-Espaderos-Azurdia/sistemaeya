document.addEventListener('DOMContentLoaded',
	function(){
		try{
			SetStyleExpediente();
			SetCheckAutenticaFirma();	
		}
		catch{
			SetCheckAutenticaFirma();		
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

function SetCheckAutenticaFirma(){

	var AutenticaFirma = document.getElementById("id_autenticafirma");	
	if(AutenticaFirma.value == 0)
	{
		SetCheckAutenticaFirmas(false);
		/*document.getElementById("id_cobro_4").checked = false;*/
	}
	else
	{
		SetCheckAutenticaFirmas(true);
		/*document.getElementById("id_cobro_4").checked = true;*/
	}

}

function SetCheckAutenticaFirmas(Valor){

	for(i =0; i<800; i++)
	{
		try{
			if(document.getElementById("id_cobro_"+i).value == 7){
				document.getElementById("id_cobro_"+i).checked = Valor;			
			}
		}
		catch{
			i = 1000;
		}
	}
}

