// map node type selector 
// control functions
// by meverest, mw@freenet.net.au, node KBN
var result = '';

function show_nodeselector()
{
    document.getElementById('nodetype_selector').style.display = 'block';
}

function hide_nodeselector()
{
    document.getElementById('nodetype_selector').style.display = 'none';
}
function mapselect_toggle( type )
{
        var active = document.getElementById('id_active').checked ? 'n' : 'y';
        var testing = document.getElementById('id_testing').checked ? 'n' : 'y';
        var building = document.getElementById('id_building').checked ? 'n' : 'y';
        var gathering = document.getElementById('id_gathering').checked ? 'n' : 'y';
        var interested = document.getElementById('id_interested').checked ? 'n' : 'y';
        var url="/ajax/toggle_nodetype.php?active="+active+"&testing="+testing+"&building="+building+"&gathering="+gathering+"&interested="+interested;
        if( active == 'y' || testing == 'y' || building == 'y' || gathering == 'y' || interested == 'y') 
            document.getElementById('all_nodes_text').innerHTML = '<img src="/images/icon_mag.png" alt="Select node types to display" border="0">Selected Nodes';
        else
            document.getElementById('all_nodes_text').innerHTML = '<img src="/images/icon_mag.png" alt="Select node types to display" border="0">All Nodes';
        result='';
	createRequest();
	xmlHttp.open("GET", url, true);
	xmlHttp.onreadystatechange = getAjaxResult;
	xmlHttp.send();
}

function getAjaxResult() {
	if(xmlHttp.readyState == 4) {
		result = xmlHttp.responseText;
		map.removeOverlay(geoXmlMap);
                geoXmlMap = new GGeoXml("http://" + location.host + "/maps/map.kml?"+result.replace(/^\s\s*/, '').replace(/\s\s*$/, ''));
                map.addOverlay(geoXmlMap);
	}
}

function  createRequest() {
	if(window.ActiveXObject) {
		xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
	} else if(window.XMLHttpRequest) {
		xmlHttp = new XMLHttpRequest();
	}
}
