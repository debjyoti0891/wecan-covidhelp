---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

<!-- ## Debjyoti Bhattacharjee ##
#### Research and Development Engineer #### -->

<!-- <p align="justify" class="introtext"><img src="/assets/me.jpg" alt="Smiley face" width="300"  align="left" style="padding-right: 20px;">
<b>Debjyoti Bhattacharjee </b> <br>
<span class="introhightext">System Level Design team, imec<br>
Kapeldreef 75,  Leuven 3001, Belgium</span>
<br>
<br>
Debjyoti Bhattacharjee is a Research and Development engineer at Compute System Architecture unit at <a href="https://www.imec.be/" target="_blank">imec</a>, Leuven. His current work focuses on design space exploration and performance estimation for high performance accelerator architectures for machine learning workloads.  -->

<div class="headHi"> West Bengal Covid Aid Network (WBCAN) </div>
<div class="introtext"> The West Bengal Covid Aid Network (WBCAN) is a citizen's initiative to try and put together resources for Covid patients across the whole of West Bengal. </div>

<div align="center">
<br><br>
<a href="{{ "/Admission/" | relative_url}}" >
    <div class="card">
        <h4><b>Hospital Bed</b></h4>
    </div>
</a>
<a href="{{ "/oxygen/" | relative_url}}" >
    <div class="card">
        <h4><b>Oxygen</b></h4>
    </div>
</a>
<a href="{{ "/test/" | relative_url}}" >
    <div class="card">
        <h4><b>Covid Test</b></h4>
    </div>
</a>
<a href="{{ "/blood/" | relative_url}}" >
    <div class="card">
        <h4><b>Blood and Plasma</b></h4>
    </div>
</a>
<a href="{{ "/tele/" | relative_url}}" >
    <div class="card">
        <h4><b>Doctor</b></h4>
    </div>
</a>
<a href="{{ "/food/" | relative_url}}" >
    <div class="card">
        <h4><b>Food</b></h4>
    </div>
</a>
<a href="{{ "/ambulance/" | relative_url}}" >
    <div class="card">
        <h4><b>Ambulance</b></h4>
    </div>
</a>

<a href="{{ "/Medicine/" | relative_url}}" >

<div class="card">
<h4><b>Medicine</b></h4>
</div>
</a>

<a href="{{ "/Quarantine/" | relative_url}}" >

<div class="card">
<h4><b>Quarantine & Home Care</b></h4>
</div>
</a>

<a href="{{ "/volunteer/" | relative_url}}" >

<div class="card">
<h4><b>Volunteers</b></h4>
</div>
</a>

</div>
<!-- <div class="privacy-card">
    <div>
        <h4>Terms of Privacy Policy</h4>
        <p>If you choose to use our Service, then you agree to the collection and use of information in relation with this policy. The Personal Information that we collect are used for providing and improving the Service. We will not use or share your information with anyone except as described in this Privacy Policy.</p>
        <div class="btns">
            <button onclick="acceptPrivacyPolicy()" class="privary-card-btn">Accept</button>
            <a href="/privacy/"><button class="privary-card-btn">Learn More</button></a>
        </div>
    </div>
</div> -->
<script>
    function acceptPrivacyPolicy() {
        window.localStorage.setItem("wbcan-privacy-polict-accepted", true)
        console.log("You accepted our terms of services")
        document.querySelector(".wrapper").removeChild(document.querySelector(".privacy-card"))
    }
    if (window.localStorage.getItem("wbcan-privacy-polict-accepted") != "true") {
        var privacyCard = document.createElement("div")
        privacyCard.classList = "privacy-card"
        privacyCard.innerHTML = `
        <div>
            <h4>Terms of Privacy Policy</h4>
            <p>If you choose to use our Service, then you agree to the collection and use of information in relation with this policy. The Personal Information that we collect are used for providing and improving the Service. We will not use or share your information with anyone except as described in this Privacy Policy.</p>
            <div class="btns">
                <button onclick="acceptPrivacyPolicy()" class="privary-card-btn">Accept</button>
                <a href="/about#privacy"><button class="privary-card-btn">Learn More</button></a>
            </div>
        </div>`
        document.querySelector(".wrapper").appendChild(privacyCard)
    }

</script>
