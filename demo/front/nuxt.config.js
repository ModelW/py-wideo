import { envManager, defineModelWConfig } from "@model-w/preset-nuxt3";

export default envManager((env) => {
    return defineModelWConfig(env, {
        siteName: "demo",
        head: {
            meta: [
                { charset: "utf-8" },
                {
                    name: "viewport",
                    content: "width=device-width, initial-scale=1",
                },
                { name: "format-detection", content: "telephone=no" },
            ],
        },
        cmsAlias: "wubba-lubba-dub-dub",
    });
});
