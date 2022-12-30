package ipca.example.smartenergy

import org.json.JSONObject

class Device {

    var iddevices       : String? = null
    var macaddress      : String? = null
    var detail          : String? = null
    var coordinatex     : String? = null
    var coordinatey     : String? = null
    var status          : String? = null


    constructor(iddevices   : String?,
                macaddress  : String?,
                detail      : String?,
                coordinatex : String?,
                coordinatey : String?,
                status      : String?) {
        this.iddevices   = iddevices
        this.macaddress  = macaddress
        this.detail      = detail
        this.coordinatex = coordinatex
        this.coordinatey = coordinatey
        this.status      = status
    }

    fun toJSON() : JSONObject {
        val jsonObject = JSONObject()
        jsonObject.put("iddevices"   , iddevices   )
        jsonObject.put("detail"      , detail      )
        jsonObject.put("macaddress"  , macaddress  )
        jsonObject.put("coordinatex" , coordinatex )
        jsonObject.put("coordinatey" , coordinatey )
        jsonObject.put("status" , status )
        return jsonObject
    }

    companion object{
        fun fromJSON(jsonObject: JSONObject) : Device {
            return Device(
                jsonObject.getString("iddevices"   ),
                jsonObject.getString("macaddress"  ),
                jsonObject.getString("detail"      ),
                jsonObject.getString("coordinatex" ),
                jsonObject.getString("coordinatey" ),
                jsonObject.getString("status"      )
            )
        }
    }

}