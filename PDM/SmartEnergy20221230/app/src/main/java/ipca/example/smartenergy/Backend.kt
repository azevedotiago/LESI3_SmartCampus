package ipca.example.smartenergy

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException

object Backend {

    private val client = OkHttpClient()
    //private const val server = "10.10.10.2"   // real tests
    private const val server = "192.168.1.40"   // home office tests

    fun fetchDevices(scope: CoroutineScope, method: String, `object`: String, callback: (ArrayList<Device>)->Unit )   {
        scope.launch (Dispatchers.IO) {
            val request = Request.Builder()
                .url("http://$server/engine.php?method=$method&object=$`object`")
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                val result =  response.body!!.string()
                Log.d(MainActivity.TAG, result)

                val jsonObject = JSONObject(result)
                if (jsonObject.getString("status") == "ok"){
                    val devices = arrayListOf<Device>()
                    val devicesJSONArray = jsonObject.getJSONArray("devices")
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

    fun fetchDeviceLog(scope: CoroutineScope, method: String, `object`: String, `params`: String,  callback: (ArrayList<DeviceLog>)->Unit )   {
        scope.launch (Dispatchers.IO) {
            val request = Request.Builder()
                .url("http://$server/engine.php?method=$method&object=$`object`&devices_iddevices=$`params`")
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                val result =  response.body!!.string()
                Log.d(MainActivity.TAG, result)

                val jsonObject = JSONObject(result)
                if (jsonObject.getString("status") == "ok"){
                    val devicesLog = arrayListOf<DeviceLog>()
                    val devicesLogJSONArray = jsonObject.getJSONArray("devicestatus")
                    for( index in 0 until devicesLogJSONArray.length()){
                        val deviceLogJSONObject = devicesLogJSONArray.getJSONObject(index)
                        val deviceLog = DeviceLog.fromJSON(deviceLogJSONObject)
                        devicesLog.add(deviceLog)
                    }
                    scope.launch (Dispatchers.Main){
                        callback(devicesLog)
                    }
                }
            }
        }
    }

    fun fetchImage(scope: CoroutineScope,
                   url: String,
                   callback: (Bitmap?)->Unit) {
        scope.launch{
            withContext(Dispatchers.IO){

                if (url.contains("http")) {
                    val request = Request.Builder()
                        .url(url)
                        .build()
                    client.newCall(request).execute().use { response ->
                        val input = response.body!!.byteStream()
                        val bitmap = BitmapFactory.decodeStream(input)
                        withContext(Dispatchers.Main) {
                            callback(bitmap)
                        }
                    }
                }
            }
        }
    }

}