<template>
    <div class="flex flex-col space-y-4">
        <div class="text-2xl">About</div>
        <div class="p-4">
            Initial Describo development was undertaken by UTS to assist researchers in describing
            research objects for archiving and publication using the RO-Crate standard. The product
            that was created proved to be so effective that it has now formed the basis of the
            description activities being undertaken by the CS3MESH4EOSC Work Package 4. In addition,
            it will form a key component of the next generation PARADISEC catalog.
        </div>
        <div class="flex flex-col space-y-4">
            <div class="flex flex-row justify-around">
                <div class="p-6">
                    <a href="https://uts.edu.au/" target="_blank">
                        <img src="images/logo-uts.svg" class="h-12" />
                    </a>
                </div>
                <div class="p-6">
                    <a href="https://paradisec.org.au/" target="_blank">
                        <img src="images/logo-paradisec.png" class="h-12" />
                    </a>
                </div>
            </div>
            <div class="flex flex-col space-y-4 lg:flex-row lg:space-y-0 justify-around">
                <div class="p-6 bg-black">
                    <a href="https://cs3mesh4eosc.eu/" target="_blank">
                        <img src="images/logo-cs3mesh4eosc.png" class="xl:h-8" />
                    </a>
                </div>
                <div class="p-6 bg-white">
                    <a href="https://www.psnc.pl" target="_blank">
                        <img src="images/logo-psnc.svg" class="xl:h-8" />
                    </a>
                </div>
            </div>
            <div class="flex flex-row justify-around">
                <div class="p-6">
                    <img src="images/logo-eu.png" class="xl:h-20" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {};
    },
};
</script>
