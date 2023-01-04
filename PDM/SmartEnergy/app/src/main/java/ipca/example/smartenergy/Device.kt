package ipca.example.smartenergy

import org.json.JSONObject

class Device {
//    #### fetchDevices...| jsonObject {"status":"ok","totalResults":"1","devicesstatus":
//    [{"iddevices":"11","macaddress":"c4:5b:be:f3:c4:8f","detail":"Poste 11","coordinatex":"41.537094","coordinatey":"-8.627941",
//    "idlogs":"217227","datetime":"2022-12-27 10:46:26","ipaddress":"10.10.10.103","valled":"0","stateled":"0","valldr":"472",
//    "valldrnew":"47","valpir":"0","statepir":"0","devices_iddevices":"11","status":"offline"}]}

    var iddevices           : String? = null
    var macaddress          : String? = null
    var detail              : String? = null
    var coordinatex         : String? = null
    var coordinatey         : String? = null
    var idlogs              : String? = null
    var datetime            : String? = null
    var ipaddress           : String? = null
    var valled              : String? = null
    var stateled            : String? = null
    var valldr              : String? = null
    var valldrnew           : String? = null
    var valpir              : String? = null
    var statepir            : String? = null
    var status              : String? = null


    constructor(iddevices           : String?,
                macaddress          : String?,
                detail              : String?,
                coordinatex         : String?,
                coordinatey         : String?,
                idlogs              : String?,
                datetime            : String?,
                ipaddress           : String?,
                valled              : String?,
                stateled            : String?,
                valldr              : String?,
                valldrnew           : String?,
                valpir              : String?,
                statepir            : String?,
                status              : String?) {
        this.iddevices          = iddevices
        this.macaddress         = macaddress
        this.detail             = detail
        this.coordinatex        = coordinatex
        this.coordinatey        = coordinatey
        this.idlogs             = idlogs
        this.datetime           = datetime
        this.ipaddress          = ipaddress
        this.valled             = valled
        this.stateled           = stateled
        this.valldr             = valldr
        this.valldrnew          = valldrnew
        this.valpir             = valpir
        this.statepir           = statepir
        this.status             = status
    }

    fun toJSON() : JSONObject {
        val jsonObject = JSONObject()
        jsonObject.put("iddevices"          , iddevices         )
        jsonObject.put("detail"             , detail            )
        jsonObject.put("macaddress"         , macaddress        )
        jsonObject.put("coordinatex"        , coordinatex       )
        jsonObject.put("coordinatey"        , coordinatey       )
        jsonObject.put("idlogs"             , idlogs            )
        jsonObject.put("datetime"           , datetime          )
        jsonObject.put("ipaddress"          , ipaddress         )
        jsonObject.put("valled"             , valled            )
        jsonObject.put("stateled"           , stateled          )
        jsonObject.put("valldr"             , valldr            )
        jsonObject.put("valldrnew"          , valldrnew         )
        jsonObject.put("valpir"             , valpir            )
        jsonObject.put("statepir"           , statepir          )
        jsonObject.put("status"             , status            )
        return jsonObject
    }

    companion object{
        fun fromJSON(jsonObject: JSONObject) : Device {
            return Device(
                jsonObject.getString("iddevices"        ),
                jsonObject.getString("macaddress"       ),
                jsonObject.getString("detail"           ),
                jsonObject.getString("coordinatex"      ),
                jsonObject.getString("coordinatey"      ),
                jsonObject.getString("idlogs"           ),
                jsonObject.getString("datetime"         ),
                jsonObject.getString("ipaddress"        ),
                jsonObject.getString("valled"           ),
                jsonObject.getString("stateled"         ),
                jsonObject.getString("valldr"           ),
                jsonObject.getString("valldrnew"        ),
                jsonObject.getString("valpir"           ),
                jsonObject.getString("statepir"         ),
                jsonObject.getString("status"           )
            )
        }
    }

}