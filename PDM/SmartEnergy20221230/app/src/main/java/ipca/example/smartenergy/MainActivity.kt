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
import android.widget.*
import androidx.lifecycle.lifecycleScope


class MainActivity : AppCompatActivity() {
    // model
    var devices      = arrayListOf<Device>()
    val adapter     = DevicesAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // remover a barra de título da aplicação
        try {
            this.supportActionBar!!.hide()
        } catch (e: NullPointerException) {
        }
        setContentView(R.layout.activity_main)

        Backend.fetchDevices(lifecycleScope, "select","devices"){
            devices = it
            adapter.notifyDataSetChanged()
        }

        val listViewDevice = findViewById<ListView>(R.id.listViewDevices)
        listViewDevice.adapter = adapter
    }



    inner class DevicesAdapter : BaseAdapter() {
        override fun getCount(): Int {
           return devices.size
        }

        override fun getItem(positon: Int): Any {
            return devices[positon]
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

            val device = devices[position]
            //println("#### MainActivity | devices[position]: "+position%2)
            if (position % 2 == 0 ) {
                // nas ROWS pares coloca o fundo a cinza claro
                rowView.setBackgroundColor(Color.parseColor("#f6f6f6"))
            }
            textViewDeviceID.text = device.iddevices
            textViewDeviceMacAddress.text = device.macaddress
            textViewDeviceDetail.text = device.detail
            textViewDeviceCoord.text = device.coordinatex+", "+ device.coordinatey
            textViewDeviceStatus.text = device.status
            if (device.status=="offline") {
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
                Log.d(TAG, "device:${device.iddevices}")
                //val intent = Intent(this@MainActivity, ArticleDetailActivity::class.java)
                //intent.putExtra("title", article.title)
                //intent.putExtra("body",article.content)
                //startActivity(intent)
                //println("#### rowView.setOnClickListner | iddevices: " +device.iddevices )
                val intent = Intent(this@MainActivity, DeviceWebDetailActivity::class.java)
                intent.putExtra(EXTRA_ARTICLE, device.toJSON().toString())
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
                Toast.makeText(this, "SmartEnergy - informações", Toast.LENGTH_LONG).show()
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    companion object {
        const val TAG = "MainActivity"
        const val EXTRA_ARTICLE = "extra_article"
    }

}