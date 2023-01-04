package ipca.example.smartenergy

import org.json.JSONObject

class DeviceLog {

    var idlogs              : String? = null
    var datetime            : String? = null
    var ipaddress           : String? = null
    var valled              : String? = null
    var stateled            : String? = null
    var valldr              : String? = null
    var valldrnew           : String? = null
    var valpir              : String? = null
    var statepir            : String? = null
    var device_iddevices    : String? = null
    var status              : String? = null

    constructor(idlogs              : String?,
                datetime            : String?,
                ipaddress           : String?,
                valled              : String?,
                stateled            : String?,
                valldr              : String?,
                valldrnew           : String?,
                valpir              : String?,
                statepir            : String?,
                device_iddevices    : String?,
                status: String?     ) {
        this.idlogs             = idlogs
        this.datetime           = datetime
        this.ipaddress          = ipaddress
        this.valled             = valled
        this.stateled           = stateled
        this.valldr             = valldr
        this.valldrnew          = valldrnew
        this.valpir             = valpir
        this.statepir           = statepir
        this.device_iddevices   = device_iddevices
        this.status             = status
    }

    fun toJSON() : JSONObject {
        val jsonObject = JSONObject()
        jsonObject.put("idlogs"             , idlogs            )
        jsonObject.put("datetime"           , datetime          )
        jsonObject.put("ipaddress"          , ipaddress         )
        jsonObject.put("valled"             , valled            )
        jsonObject.put("stateled"           , stateled          )
        jsonObject.put("valldr"             , valldr            )
        jsonObject.put("valldrnew"          , valldrnew         )
        jsonObject.put("valpir"             , valpir            )
        jsonObject.put("statepir"           , statepir          )
        jsonObject.put("device_iddevices"   , device_iddevices  )
        jsonObject.put("status"             , status            )
        return jsonObject
    }

    companion object{
        fun fromJSON(jsonObject: JSONObject) : DeviceLog {
            return DeviceLog(
                jsonObject.getString("idlogs"           ),
                jsonObject.getString("datetime"         ),
                jsonObject.getString("ipaddress"        ),
                jsonObject.getString("valled"           ),
                jsonObject.getString("stateled"         ),
                jsonObject.getString("valldr"           ),
                jsonObject.getString("valldrnew"        ),
                jsonObject.getString("valpir"           ),
                jsonObject.getString("statepir"         ),
                jsonObject.getString("device_iddevices" ),
                jsonObject.getString("status"           )
            )
        }
    }
}