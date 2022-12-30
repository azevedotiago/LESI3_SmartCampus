package ipca.example.smartenergy

import android.annotation.SuppressLint
import android.content.Intent
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import android.webkit.WebView
import android.widget.BaseAdapter
import android.widget.TextView
import androidx.lifecycle.lifecycleScope
import org.json.JSONObject

class DeviceWebDetailActivity : AppCompatActivity() {

    var device : Device? = null
    var devicesLog  = arrayListOf<DeviceLog>()
    private val adapterLog     = DevicesLogAdapter()

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_device_web_detail)
        device = Device.fromJSON(JSONObject(intent.getStringExtra(MainActivity.EXTRA_ARTICLE).toString()))
        println("#### DeviceWebDetailActivity | device: "+device?.iddevices)
        title = device?.iddevices + " - " + device?.detail + " ("+ device?.macaddress + ")"
        println("#### DeviceWebDetailActivity | title: $title")
/*
        Backend.fetchDeviceLog(lifecycleScope, "select","devicestatus",device?.iddevices.toString()){
            println("#### DeviceWebDetailActivity | Backend.fetchDeviceLog ")
            devicesLog = it
            adapterLog.notifyDataSetChanged()
        }
*/

        findViewById<TextView>(R.id.textViewDeviceID).text          =  device?.iddevices
        findViewById<TextView>(R.id.textViewDeviceMacAddress).text  =  device?.macaddress
        findViewById<TextView>(R.id.textViewDeviceDetail).text      =  device?.detail
        findViewById<TextView>(R.id.textViewDeviceCoord).text       =  device?.coordinatex+", "+device?.coordinatey
        findViewById<TextView>(R.id.textViewDeviceLogsStatus).text  =  device?.status
        if (device?.status=="offline") {
            // cor do texto vermelho para o estado offline
            findViewById<TextView>(R.id.textViewDeviceLogsStatus).setTextColor(Color.parseColor("#E91E63"));
        } else {
            // cor do texto verde para o estado online
            findViewById<TextView>(R.id.textViewDeviceLogsStatus).setTextColor(Color.parseColor("#228B22"));
        }

        println("#### DeviceWebDetailActivity | textView")
        println("#### -> " + findViewById<TextView>(R.id.textViewDeviceID).text)

    }

    inner class DevicesLogAdapter : BaseAdapter() {
        override fun getCount(): Int {
            return devicesLog.size
        }

        override fun getItem(positon: Int): Any {
            return devicesLog[positon]
        }

        override fun getItemId(positon: Int): Long {
            return 0L
        }

        @SuppressLint("SetTextI18n")
        override fun getView(position: Int, view: View?, parent: ViewGroup?): View {
            val rowView = layoutInflater.inflate(R.layout.row_device,parent, false)
            val textViewDeviceID = rowView.findViewById<TextView>(R.id.textViewDeviceID)
            val textViewDeviceMacAddress = rowView.findViewById<TextView>(R.id.textViewDeviceMacAddress)
            val textViewDeviceDetail = rowView.findViewById<TextView>(R.id.textViewDeviceDetail)
            val textViewDeviceCoord = rowView.findViewById<TextView>(R.id.textViewDeviceCoord)
            val textViewDeviceStatus = rowView.findViewById<TextView>(R.id.textViewDeviceStatus)

            val deviceLog = devicesLog[position]
            //println("#### MainActivity | devices[position]: "+position%2)
            if (position % 2 == 0 ) {
                // nas ROWS pares coloca o fundo a cinza claro
                rowView.setBackgroundColor(Color.parseColor("#f6f6f6"))
            }
            /*
            textViewDeviceID.text = deviceLog.iddevices
            textViewDeviceMacAddress.text = deviceLog.macaddress
            textViewDeviceDetail.text = deviceLog.detail
            textViewDeviceCoord.text = deviceLog.coordinatex+", "+ deviceLog.coordinatey
            textViewDeviceStatus.text = deviceLog.status*/
            if (deviceLog.status=="offline") {
                // cor do texto vermelho para o estado offline
                textViewDeviceStatus.setTextColor(Color.parseColor("#E91E63"));
            } else {
                // cor do texto verde para o estado online
                textViewDeviceStatus.setTextColor(Color.parseColor("#228B22"));
            }


            //textViewDeviceStatus.textColors = "@android:color/holo_green_dark"


            /*
            device.status?.let {
                Backend.fetchImage(lifecycleScope, it){ bitmap ->
                    imageViewDevice.setImageBitmap(bitmap)
                }
            }*/


            rowView.setOnClickListener {
                Log.d(MainActivity.TAG, "device:${device?.iddevices}")
                //val intent = Intent(this@MainActivity, ArticleDetailActivity::class.java)
                //intent.putExtra("title", article.title)
                //intent.putExtra("body",article.content)
                //startActivity(intent)
                //println("#### rowView.setOnClickListner | iddevices: " +device.iddevices )
                val intent = Intent(this@DeviceWebDetailActivity, DeviceWebDetailActivity::class.java)
                intent.putExtra(MainActivity.EXTRA_ARTICLE, device?.toJSON().toString())
                //println("#### rowView.setOnClickListner | intent: "+device.toJSON().toString())
                startActivity(intent)
            }
            return rowView
        }

    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_device,menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when(item.itemId){
            R.id.action_share -> {
                val intent = Intent(Intent.ACTION_SEND)
                intent.putExtra(Intent.EXTRA_TEXT, device?.coordinatey)
                intent.type = "text/plain"
                val intentChooser = Intent.createChooser(intent, device?.iddevices)
                startActivity(intentChooser)
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}