package ipca.example.smartenergy

import android.content.Intent
import android.text.Editable
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException

object Backend {

    private val client = OkHttpClient()
    private const val server = "10.10.10.2"   // real tests
    //private const val server = "192.168.1.40"   // home office tests

    fun fetchDevices(scope: CoroutineScope, method: String, `object`: String, callback: (ArrayList<Device>)->Unit )   {
        scope.launch (Dispatchers.IO) {
            val request = Request.Builder().url("http://$server/engine.php?method=$method&object=$`object`").build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                val result =  response.body!!.string()
                Log.d(MainActivity.TAG, result)
                //println("#### fetchDevices...")
                val jsonObject = JSONObject(result)
                //println("#### fetchDevices...| jsonObject "+ jsonObject.toString())
                if (jsonObject.getString("status") == "ok"){
                    val devices = arrayListOf<Device>()
                    val devicesJSONArray = jsonObject.getJSONArray("devicesstatus")  // devices or devicestatus
                    for( index in 0 until devicesJSONArray.length()){
                        val deviceJSONObject = devicesJSONArray.getJSONObject(index)
                        val device = Device.fromJSON(deviceJSONObject)
                        devices.add(device)
                    }
                    scope.launch (Dispatchers.Main){
                        callback(devices)
                    }
                }
            }
        }
    }

    fun login(
        scope: CoroutineScope,
        method: String,
        username: Editable,
        password: Editable,
        callback: (Boolean) -> Unit
    ) :Boolean  {
        var loginStatus : Boolean = false
        scope.launch (Dispatchers.IO) {
            val request = Request.Builder().url("http://$server/login.php?method=$method&username=$username&password=$password").build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                val result =  response.body!!.string()
                Log.d(MainActivity.TAG, result)
                //println("#### Backend.login...")
                val jsonObject = JSONObject(result)
                //println("#### Backend.login...| jsonObject $jsonObject")
                if (jsonObject.getString("response") == "true"){
                    loginStatus = true
                }
                scope.launch (Dispatchers.Main){
                    callback(loginStatus)
                }
            }
        }
        //println("#### Backend.login...| response: $loginStatus")
        return loginStatus
    }
}