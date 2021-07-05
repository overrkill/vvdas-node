const prompt = require("prompt-sync")({sigint:true})
const axios = require("axios")
const fs= require('fs')
const chalk = require('chalk')
// const URI = "http://localhost:3000/api/"
const URI = "https://virt-api.herokuapp.com/api/"

// definitions
const log = console.log
const vehicle_details = {
    model : "",
    vehicle_type : "",
    purchased_on : "",
    fuel_type : "",
    engine_no : "",
    chasis_no : "",
    rc_no : ""
}



console.clear()
log(chalk.blackBright.bgCyanBright.bold("VIRTUOSO Node initialization setup"))
log(chalk.red.bold("**only for use by RTO/Authority**"))
log("---------------------------------------\n\n")


if(fs.existsSync("../node/id") && fs.existsSync("../node/pvk") && fs.existsSync("../node/vid")){
        log(chalk.redBright.bold.italic("NODE ALREADY INITIALIZED"))
        log(chalk.italic("incase of any issues contact RTO"))
} else {
  
const owner_dl = prompt("Owner Driving license no. -- ")
log(`you entered "${owner_dl}"`)

    axios.get(URI+"license/user/"+owner_dl).then(
        data =>{
            fs.writeFileSync("../node/owner_details.json", JSON.stringify(data.data))
            
            log(chalk.greenBright("Success! License found"))
            
            setTimeout(()=>{
                console.clear()
           
            const token = prompt(chalk.green("enter Authorization token"), {echo:"*"})

            const node_id = prompt("Node ID -- ")
            log(`you entered "${node_id}"`)

            // do verify license exist

            // get vehicle details
            console.clear()
            log(chalk.blackBright.bgCyanBright.bold("VIRTUOSO Node initialization setup"))
            log(chalk.whiteBright.bgBlackBright.bold("\n-- Enter Vehicle Details --\n"))
            vehicle_details.model = prompt("Model -- ")
            vehicle_details.vehicle_type = prompt("Vehicle Type -- ")
            vehicle_details.purchased_on = new Date(prompt("purchased on(yyyy-mm-dd) -- ")).toISOString()
            vehicle_details.fuel_type = prompt("fuel type -- ")
            vehicle_details.engine_no = prompt("engine no -- ")
            vehicle_details.chasis_no = prompt("chasis no -- ")
            vehicle_details.rc_no = prompt("RC no -- ")


            fs.writeFileSync("../node/id",node_id)
            fs.writeFileSync("../node/vehicle_details.json", JSON.stringify(vehicle_details))
            axios.post(URI+"auth/createnode",{
                nodeId  : node_id,
                createdBy : token
            }).then(res=>{
                fs.writeFileSync("../node/vid",res.data.virtTd)
                fs.writeFileSync("../node/pvk",res.data.pvKey)
                log(chalk.green("Node initialized successfully"))
            }).catch(err=>{
                console.error(err);
            })
        },1000)
        }
    ).catch(
        err=>{
            log(chalk.red("License not found try again"))
        }
    )


}


